"""lebut - Lektor Butler. Lektor + customizations."""
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime
from string import Template
from typing import List

import fire

from lebut import lektor_monkeypatch, livereloader
from lebut.config import NAME, PATH
from lektor.cli import clean_cmd, build_cmd, deploy_cmd

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
lektor_monkeypatch.patch_all()
os.environ["LEKTOR_OUTPUT_PATH"] = str(PATH.OUTPUT)
PORT = "5000"


def main():
    oldPath = os.getcwd()
    try:
        os.chdir(str(PATH.PROJECT))
        fire.Fire(Workflow())
    finally:
        os.chdir(oldPath)


class Workflow:
    """Home baked blog create, dev, publish workflow"""

    @classmethod
    def new(cls, slug: str):
        assert " " not in slug, f"expected wanted slug (rel url)"
        assert not (PATH.DRAFTS / slug).exists(), "already in drafts"
        container = PATH.ARTICLES / slug
        container.mkdir()
        (container / NAME.DRAFT).write_text("")
        content = (PATH.HERE / "contents-tpl.lr").read_text()
        content = Template(content).safe_substitute(
            dict(title=slug, date=datetime.now().strftime("%Y-%m-%d"))
        )
        (container / NAME.CONTENTS).write_text(content)
        log.info("hint: to finish this up run tox -e serve --drafts")

    @classmethod
    def clean(cls):
        cls._move_drafts(PATH.ARTICLES, PATH.DRAFTS)
        sys.argv = ["xxx", "-vvvv", "--yes"]
        cls._dont_kill_me(clean_cmd)
        if PATH.OUTPUT.exists():
            shutil.rmtree(PATH.OUTPUT)

    @classmethod
    def serve(cls, drafts=False):
        """let lektor rebuild but use livereload plugin, instead of inbuilt server."""
        sys.argv = ["xxx", "--watch", "-vvvv"]
        # os.environ["LEKTOR_DEV"] = "1"
        if drafts:
            cls._move_drafts(PATH.DRAFTS, PATH.ARTICLES)
        try:
            livereloader.LiveReloader().start(PORT)
            build_cmd()
        finally:
            if drafts:
                cls._move_drafts(PATH.ARTICLES, PATH.DRAFTS)

    @classmethod
    def build(cls, clean=False):
        if clean:
            cls.clean()
        sys.argv = ["xxx", "-vvvv"]
        cls._dont_kill_me(build_cmd)

    @classmethod
    def deploy(cls):
        cls._move_drafts(PATH.ARTICLES, PATH.DRAFTS)
        cls.build(clean=True)
        sys.argv = ["xxx"]
        deploy_cmd()

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

    @classmethod
    def _dont_kill_me(cls, function):
        try:
            function()
        except SystemExit as e:
            assert e.code == 0, e.code


if __name__ == "__main__":
    sys.argv = ["lebut", "serve"]
    main()
