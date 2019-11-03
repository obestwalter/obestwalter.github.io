import hashlib
import json
import logging
import os
import sys

from pathlib import Path

import nbconvert
import nbformat
from IPython import InteractiveShell
from IPython.core.magics import CodeMagics
from nbconvert.preprocessors import ExecutePreprocessor

from lebut import PATH, NAME, URL

log = logging.getLogger(__name__)

_CACHE_PATH: Path = Path(__file__).with_suffix(".json")
try:
    CACHE = json.loads(_CACHE_PATH.read_text())
except FileNotFoundError:
    CACHE = {}

IPYTHON_SHELL = InteractiveShell()

def process_all(container):
    try:
        for path in [
            p
            for p in container.glob("**/*.ipynb")
            if ".ipynb_checkpoints" not in p.parts
        ]:
            process(container, path)
    finally:
        _CACHE_PATH.write_text(json.dumps(CACHE))


def process(container, path, force=False):
    content = path.read_text()
    oldHash = CACHE.get(str(path.relative_to(container)))
    newHash = hashlib.sha256(content.encode()).hexdigest()
    newPath = path.parent / NAME.CONTENTS
    if not force and newHash == oldHash and newPath.exists():
        log.info(f"[SKIP] {path} - did not change")
        return

    CACHE[str(path.relative_to(container))] = newHash
    newPath.write_text(convert(path))


def convert(path):
    filename = path.name
    cwd = path.parent
    log.info(f"convert to markdown: {filename}")
    resources = {"fileRelPath": f"{cwd.name}/{filename}"}
    nb = nbformat.reads(path.read_text(), as_version=4)
    oldPath = os.getcwd()
    try:
        os.chdir(cwd)
        preproc = ArticleExecutePreprocessor(
            timeout=600, kernel_name="python3", resources=resources
        )
        preproc.preprocess(nb, resources=resources)
    finally:
        os.chdir(oldPath)
    return nbconvert.MarkdownExporter().from_notebook_node(nb, resurces=resources)[0]


class ArticleExecutePreprocessor(ExecutePreprocessor):
    """Massage the code cell outputs to suit the blog.

    I'm sure there are more elegant ways, but this works for me atm.
    """

    def preprocess(self, nb, resources=None, km=None):
        srcUrl = f"{URL.WEBSITE_ARTICLES}/{resources['fileRelPath']}"
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        source = (
            f"!!! This article is generated from a "
            f"[Jupyter notebook](https://jupyter.org/) "
            f"running in a Python {version} kernel. "
            f"You can [download it]({srcUrl}) and play with it."
        )
        cell = nbformat.NotebookNode(
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": source,
            }
        )
        nb.cells.append(cell)
        super().preprocess(nb, resources=resources, km=km)

    def preprocess_cell(
            self, cell, resources, cell_index, store_history=True
    ):
        if cell.cell_type != "code":
            return cell, resources

        assert isinstance(cell.source, str)
        load_candidate = cell.source.replace("# ", "")
        if load_candidate.startswith("%load"):
            cell.source = self.apply_load_magic(load_candidate)
            return cell, resources

        _, outs = self.run_cell(cell, cell_index, store_history)
        new = [f"\n\n```python\n{cell.source}\n```"]
        for o in outs:
            if o.output_type == "execute_result":
                # TODO deal with other types as they come up
                data = o.data["text/plain"]
                new.append(f"```text\n[result]\n{data}```")
            elif o.output_type == "error":
                new.append(f"```text\n[{o.ename}]\n{o.evalue}```")
            elif o.output_type == "stream":
                new.append(f"```text\n[{o.name}]\n{o.text}```")
            else:
                raise Exception(f"dunno what to do with: {o}")
        cell = nbformat.NotebookNode(
            {
                "cell_type": "raw",
                "metadata": {},
                "source": "\n".join(new)
            }
        )
        return cell, resources

    def apply_load_magic(self, content):
        """Apply the %load magic manually.

        Cell magic is not automatically applied by
        the preprocessor, so I do this directly here.

        I'm sure this is horribly wrong, but it works well enough.
        """
        magic = CodeMagics(shell=IPYTHON_SHELL)
        arg_s = " ".join(content.split()[1:])
        magic.load(arg_s)
        code = IPYTHON_SHELL.rl_next_input
        return code


if __name__ == "__main__":
    # quick and dirty ad-hoc testing
    logging.basicConfig(level=logging.INFO)
    CACHE = {}
    # process_all(PATH.DRAFTS)
    p = PATH.HERE / "example-notebook.ipynb"
    process(p.parent, p)
