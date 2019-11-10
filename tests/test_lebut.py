"""Primitive high level tests: if nothing crashes things look good."""
from pathlib import Path

import pytest

import lektor.pluginsystem
from lebut.config import PATH
from lebut.lektor_monkeypatch import initialize_plugins_with_local_plugins
from lebut.plugin_ipynb_to_md import source_obj_to_ipynb
from lektor.builder import Builder
from lektor.cli import build_cmd, clean_cmd
from lektor.db import Query, Page
from lektor.reporter import CliReporter

# duplicated knowledge -> not worth fixture or shared importable module
HERE = Path(__file__).parent
OUTPUT_PATH = HERE / "build"
PROJECT_PATH = HERE / "project"


@pytest.fixture
def patched_plugins(monkeypatch):
    monkeypatch.setattr(
        lektor.pluginsystem, "initialize_plugins", initialize_plugins_with_local_plugins
    )


@pytest.mark.xfail(
    reason="jinja2.exceptions.UndefinedError: 'get_pygments_stylesheet' is undefined"
)
@pytest.mark.parametrize(
    "slug, root",
    (
        # ("about", "/"),
        ("notebook-post", "blog"),
    ),
)
@pytest.mark.usefixtures("patched_plugins")
def test_single_page_build(env, slug, root):
    reporter = CliReporter(env, verbosity=4)
    with reporter:
        env.load_plugins()
        pad = env.new_pad()
        builder = Builder(pad, OUTPUT_PATH)
        query = Query(root, pad)
        page: Page = query.get(slug)
        assert page
        for attachment in page.attachments:
            source_obj_to_ipynb(attachment)
        # FIXME make fail and make sure error bubbles up
        builder.build(page)
        # FIXME generating actual html does not yield anything this way
        # out = Path(project.get_output_path()) / page.path[1:] / "index.html"
        # text = out.read_text()
        # assert len(text) > 100


@pytest.mark.xfail(
    reason="jinja2.exceptions.UndefinedError: 'get_pygments_stylesheet' is undefined"
)
@pytest.mark.usefixtures("patched_plugins")
def test_complete_build_test_project(monkeypatch):
    monkeypatch.chdir(PROJECT_PATH)
    build_cmd(["-vvvv", "--output-path", str(OUTPUT_PATH)])


@pytest.mark.usefixtures("patched_plugins")
def test_complete_build_my_site(monkeypatch):
    monkeypatch.chdir(PATH.PROJECT)
    try:
        clean_cmd(["--yes", "-vvvv", "--output-path", str(PATH.OUTPUT)])
    except SystemExit as e:
        assert e.code == 0

    try:
        build_cmd(["-vvvv", "--output-path", str(OUTPUT_PATH)])
    except SystemExit as e:
        assert e.code == 0
