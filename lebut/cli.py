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
from slugify import slugify

from lebut import lektor_monkeypatch, livereloader
from lebut.config import NAME, PATH
from lektor.cli import clean_cmd, build_cmd, deploy_cmd

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
lektor_monkeypatch.patch_all()


def main():
    oldPath = os.getcwd()
    try:
        os.chdir(str(PATH.PROJECT))
        fire.Fire(Workflow())
    finally:
        os.chdir(oldPath)


class Workflow:
    """Home baked log creation, adaption, publishing workflow"""

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
    def clean(cls):
        sys.argv = ["xxx", "-vvvv", "--yes", "--output-path", str(PATH.OUTPUT)]
        clean_cmd()
        if PATH.OUTPUT.exists():
            shutil.rmtree(PATH.OUTPUT)

    @classmethod
    def serve(cls):
        """let lektor rebuild but use livereload plugin, instead of inbuilt server."""
        sys.argv = ["xxx", "--watch", "-vvvv", "--output-path", str(PATH.OUTPUT)]
        # os.environ["LEKTOR_DEV"] = "1"
        cls._move_drafts(PATH.DRAFTS, PATH.ARTICLES)
        try:
            livereloader.LiveReloader().start()
            build_cmd()
        finally:
            cls._move_drafts(PATH.ARTICLES, PATH.DRAFTS)

    @classmethod
    def build(cls, clean=False):
        if clean:
            try:
                cls.clean()
            except SystemExit as e:
                assert e.code == 0, e.code

        sys.argv = ["xxx", "-vvvv", "--output-path", str(PATH.OUTPUT)]
        build_cmd()

    @classmethod
    def deploy(cls):
        sys.argv = ["xxx", "--output-path", str(PATH.OUTPUT)]
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


if __name__ == "__main__":
    sys.argv = ["lebut", "serve"]
    main()
