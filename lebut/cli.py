""" lebut - my little lektor butler to make common activities less tedious."""
import logging
import subprocess
from datetime import datetime
from io import BytesIO
from pathlib import Path
from string import Template

from lektor.admin.modules import serve
from lektor.cli import Context
from lektor.devserver import run_server
from lektor.utils import slugify

from lebut.compile_notebooks import JupyterNbConvert

# I don't use the editor - get rid of the button during development
serve.rewrite_html_for_editing = lambda fp, edit_url: BytesIO(fp.read())


class PATH:
    HERE: Path = Path(__file__).parent
    PROJECT: Path = HERE.parent
    DRAFTS: Path = PROJECT / "drafts"
    CONTENT: Path = PROJECT / "content" / "articles"
    OUTPUT: Path = HERE.parent / "website_build"


log = logging.getLogger(__name__)


class Workflow:
    """blog creation, adaption, publishing workflow"""

    DRAFTMARKER = "__draft__"
    CONTENST_FILE = "contents.lr"
    myFlags = ["sass"]

    @classmethod
    def serve(
        cls,
        host="0.0.0.0",
        port=8080,
        outputPath=PATH.OUTPUT,
        verbosity=0,
        dev=True,
        reinstall=False,
        browse=False,
        prune=True,
        flags=("sass",),
    ):
        """
        :param verbosity: 0-4
        """
        assert all(f in cls.myFlags for f in flags), flags
        ctx = Context()
        ctx.load_plugins(reinstall=reinstall)
        env = ctx.get_env()
        outputPath = Path(outputPath)
        log.info(f"project: {ctx.get_project().project_path} | output: {outputPath}")
        cls.move_drafts(PATH.DRAFTS, PATH.CONTENT)
        cls.compile_notebooks()
        try:
            run_server(
                (host, port),
                env,
                outputPath,
                verbosity=verbosity,
                lektor_dev=dev,
                browse=browse,
                prune=prune,
                extra_flags=flags,
                ui_lang=ctx.ui_lang,
            )
        finally:
            cls.move_drafts(PATH.CONTENT, PATH.DRAFTS)

    @classmethod
    def move_drafts(cls, src, dst):
        for path in src.iterdir():
            if not path.is_dir():
                continue
            if (path / cls.DRAFTMARKER).exists():
                newPath = dst / path.name
                assert not newPath.exists(), newPath
                log.info(f"{path} -> {newPath}")
                path.rename(newPath)

    @classmethod
    def compile_notebooks(cls):
        JupyterNbConvert().convert()

    @classmethod
    def build(cls):
        cls.move_drafts(PATH.DRAFTS, PATH.CONTENT)
        cls.compile_notebooks()
        log.info(subprocess.check_output(["lektor", "build"]))

    @classmethod
    def deploy(cls):
        cls.move_drafts(PATH.CONTENT, PATH.DRAFTS)
        cls.compile_notebooks()
        first = subprocess.check_output(["lektor", "build"])
        second = subprocess.check_output(["lektor", "deploy"])
        log.info(first.decode() + "\n" + second.decode())

    @classmethod
    def new(cls, title):
        container = PATH.CONTENT / slugify(title)
        assert not container.exists(), container
        container.mkdir()
        (container / cls.DRAFTMARKER).write_text("")
        content = (PATH.HERE / cls.CONTENST_FILE).read_text()
        content = Template(content).safe_substitute(
            dict(title=title, date=datetime.now().strftime("%Y-%m-%d"))
        )
        (container / cls.CONTENST_FILE).write_text(content)

    @classmethod
    def clean(cls):
        log.info(subprocess.check_output(["lektor", "clean", "--yes"]))
        cls.move_drafts(PATH.CONTENT, PATH.DRAFTS)


def main():
    import fire

    logging.basicConfig(level=logging.INFO)
    fire.Fire(Workflow)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Workflow.move_drafts(PATH.DRAFTS, PATH.CONTENT)
    Workflow.move_drafts(PATH.CONTENT, PATH.DRAFTS)
