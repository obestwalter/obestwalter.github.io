"""Primitive high level tests: if nothing crashes things look good."""
import shutil
from pathlib import Path

import pytest

import lektor.pluginsystem
from lebut.lektor_monkeypatch import initialize_plugins_with_local_plugins
from lektor.builder import Builder
from lektor.db import Query, Page
from lektor.project import Project
from lektor.reporter import CliReporter

HERE = Path(__file__).parent
OUTPUT_PATH = HERE / "build"
PROJECT_PATH = HERE.parent


@pytest.fixture(scope="session", autouse=True)
def prepare_for_tests():
    # no tidying up necessary- will never use original
    lektor.pluginsystem.initialize_plugins = initialize_plugins_with_local_plugins
    shutil.rmtree(OUTPUT_PATH, ignore_errors=True)


@pytest.fixture
def project():
    project = Project.from_path(PROJECT_PATH)
    project.get_output_path = lambda *_: OUTPUT_PATH
    assert project
    return project


@pytest.mark.parametrize(
    "slug, root",
    (
        ("/", "/"),
        ("website-meta", "articles"),
    ),
)
def test_build(project, slug, root):
    # for partial tests and debugging
    env = project.make_env()
    reporter = CliReporter(env, verbosity=4)
    with reporter:
        pad = env.new_pad()
        builder = Builder(pad, OUTPUT_PATH)
        query = Query(root, pad)
        page: Page = query.get(slug)
        assert page
        builder.build(page)
        path = OUTPUT_PATH / page.path[1:] / "index.html"
        text = path.read_text()
        assert len(text) > 100  # yes, I know ...


# testing through click is pretty awful on first sight... look into this later
#
# def test_complete_build_test_project(monkeypatch):
#     monkeypatch.chdir(PROJECT_PATH)
#     build_cmd(["-vvvv", "--output-path", str(OUTPUT_PATH)])
#
#
# def test_complete_build_my_site(monkeypatch):
#     monkeypatch.chdir(PATH.PROJECT)
#     try:
#         clean_cmd(["--yes", "-vvvv", "--output-path", str(PATH.OUTPUT)])
#     except SystemExit as e:
#         assert e.code == 0
#
#     try:
#         build_cmd(["-vvvv", "--output-path", str(OUTPUT_PATH)])
#     except SystemExit as e:
#         assert e.code == 0
