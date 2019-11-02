""" lebut - my little lektor butler to make common activities less tedious."""
import logging
import os
import shutil
import subprocess
from datetime import datetime
from io import BytesIO
from string import Template
from typing import List

import fire
from slugify import slugify

from lebut import PATH, NAME
from lebut import ipynb_to_md
from lektor.admin.modules import serve
from lektor.cli import Context
from lektor.devserver import run_server

log = logging.getLogger(__name__)

# I don't use the editor - get rid of the button during development
serve.rewrite_html_for_editing = lambda fp, edit_url: BytesIO(fp.read())


def main():
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(Workflow)


class Workflow:
    """blog creation, adaption, publishing workflow"""

    MY_FLAGS = ["sass"]

    @classmethod
    def serve(
            cls,
            host="0.0.0.0",
            port=8080,
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
        assert all(f in cls.MY_FLAGS for f in flags), flags
        os.environ["WERKZEUG_RUN_MAIN"] = "true"  # avoid webpack watch
        ctx = Context()
        ctx.load_plugins(reinstall=reinstall)
        log.info(f"project: {ctx.get_project().project_path} | output: {PATH.OUTPUT}")
        cls._move_drafts(PATH.DRAFTS, PATH.ARTICLES)
        cls.compile_notebooks()
        try:
            run_server(
                bindaddr=(host, port),
                env=ctx.get_env(),
                output_path=PATH.OUTPUT,
                verbosity=verbosity,
                lektor_dev=dev,
                browse=browse,
                prune=prune,
                extra_flags=flags,
                ui_lang=ctx.ui_lang,
            )
        finally:
            cls._move_drafts(PATH.ARTICLES, PATH.DRAFTS)

    @classmethod
    def new(cls, title: str):
        container = PATH.ARTICLES / slugify(title)
        assert not container.exists(), f"{container} already exists!"
        container.mkdir()
        (container / NAME.DRAFT).write_text("")
        content = (PATH.HERE / NAME.CONTENTS).read_text()
        content = Template(content).safe_substitute(
            dict(title=title, date=datetime.now().strftime("%Y-%m-%d"))
        )
        (container / NAME.CONTENTS).write_text(content)

    @classmethod
    def compile_notebooks(cls):
        ipynb_to_md.process_all(PATH.ARTICLES)

    @classmethod
    def clean(cls):
        if ipynb_to_md._CACHE_PATH.exists():
            ipynb_to_md._CACHE_PATH.unlink()

        if PATH.OUTPUT.exists():
            shutil.rmtree(PATH.OUTPUT)
        cls._move_drafts(PATH.ARTICLES, PATH.DRAFTS)
        cls._run(["lektor", "clean", "--yes"])

    @classmethod
    def build(cls, clean=False):
        if clean:
            cls.clean()
        cls.compile_notebooks()
        cls._run(["lektor", "build", "--output-path", str(PATH.OUTPUT)])

    @classmethod
    def deploy(cls):
        cls.build()
        cls._run(["lektor", "deploy", "--output-path", str(PATH.OUTPUT)])

    @classmethod
    def html_tidy(cls):
        # FIXME not used yet: atm generated html needs manual intervention.
        for path in PATH.OUTPUT.glob("**/*.html"):
            log.info(f"tidy up {path}")
            cls._run(["tidy", "-q", "-utf8", "-o", str(path), str(path)])

    @classmethod
    def _run(cls, cmd: List[str]):
        log.debug("run: " + " ".join(cmd))
        log.info(subprocess.check_output(cmd).decode())

    @classmethod
    def _move_drafts(cls, src, dst):
        for path in src.iterdir():
            if not path.is_dir():
                continue
            if (path / NAME.DRAFT).exists():
                newPath = dst / path.name
                assert not newPath.exists(), newPath
                log.info(
                    f"{path.relative_to(PATH.PROJECT)} -> "
                    f"{newPath.relative_to(PATH.PROJECT)}"
                )
                path.rename(newPath)


if __name__ == "__main__":
    # for debugging
    logging.basicConfig(level=logging.INFO)
    oldPath = os.getcwd()
    try:
        os.chdir(str(PATH.PROJECT))
        Workflow.serve()
    finally:
        os.chdir(oldPath)
