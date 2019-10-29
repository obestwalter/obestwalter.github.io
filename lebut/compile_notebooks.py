import hashlib
import json
import logging
import sys

import nbconvert
import nbformat
from IPython.core import interactiveshell
from nbconvert.preprocessors import ExecutePreprocessor

from lebut import PATH

log = logging.getLogger(__name__)

# TODO figure out the styling (exceptions and input/output cell differentiation (maybe just a different fence mode for output ... e.g. console and style that differently))

# FIXME this approach does not work - figure out why.
def _error_only_traceback_to_stderr(self, *args, **kwargs):
    excType, msg = sys.exc_info()[:2]
    sys.stderr.write(f"{excType.__name__}: {msg}")


REAL_TB_FUNC = interactiveshell.InteractiveShell.showtraceback


class JupyterNbConvert:
    """Convert changed .ipynb to .lr files before lektor build starts."""

    CACHE_PATH = PATH.HERE / "compile_notebooks_cache.json"

    def __init__(self):
        assert PATH.ARTICLES.exists(), PATH.ARTICLES
        try:
            self.cache = json.loads(self.CACHE_PATH.read_text())
        except FileNotFoundError:
            self.cache = {}
            self.CACHE_PATH.write_text(json.dumps(self.cache))
        self.ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        self.ep.allow_errors = True

    def convert(self):
        interactiveshell.InteractiveShell.showtraceback = _error_only_traceback_to_stderr
        try:
            for path in [
                p
                for p in PATH.ARTICLES.glob("**/*.ipynb")
                if ".ipynb_checkpoints" not in p.parts
            ]:
                self.process_nb(path)
        finally:
            self.CACHE_PATH.write_text(json.dumps(self.cache))
            interactiveshell.InteractiveShell.showtraceback = REAL_TB_FUNC

    def process_nb(self, path):
        text = path.read_text()
        oldHash = self.cache.get(str(path.relative_to(PATH.ARTICLES)))
        newHash = hashlib.sha256(text.encode()).hexdigest()
        newPath = path.parent / "contents.lr"
        if newHash == oldHash and newPath.exists():
            log.info(f"[SKIP] {path} - did not change")
            return

        self.cache[str(path.relative_to(PATH.ARTICLES))] = newHash
        nb = nbformat.reads(text, as_version=4)
        self.ep.preprocess(nb, resources={"metadata": {"run_path": str(path.parent)}})
        output, _ = nbconvert.MarkdownExporter().from_notebook_node(nb)
        # log.debug(f"writing to {newPath}:\n\n{output}\n\n")
        newPath.write_text(output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from lebut.cli import Workflow
    Workflow._move_drafts(PATH.DRAFTS, PATH.ARTICLES)
    try:
        if JupyterNbConvert.CACHE_PATH.exists():
            JupyterNbConvert.CACHE_PATH.unlink()
        JupyterNbConvert().convert()
    finally:
        Workflow._move_drafts(PATH.ARTICLES, PATH.DRAFTS)
