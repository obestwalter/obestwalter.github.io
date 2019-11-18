# import shutil
# from pathlib import Path
#
# import pytest
#
# from lektor.admin.webui import WebUI
# from lektor.builder import Builder
# from lektor.db import Database
# from lektor.environment import Environment
# from lektor.project import Project
#
# # duplicated knowledge -> not worth fixture or shared importable module
# HERE = Path(__file__).parent
# OUTPUT_PATH = HERE / "build"
# PROJECT_PATH = HERE / "project"
#
#
# def make_test_project():
#     project = Project.from_path(PROJECT_PATH)
#     project.get_output_path = lambda *_: OUTPUT_PATH
#     assert project
#     return project
#
#
# @pytest.fixture
# def build_path():
#     path = HERE / "build"
#     shutil.rmtree(path, ignore_errors=True)
#     assert not path.exists()
#     return path
#
#
# @pytest.fixture
# def project():
#     return make_test_project()
#
#
# @pytest.fixture
# def env(project):
#     return Environment(project)
#
#
# @pytest.fixture
# def pad(env):
#     return Database(env).new_pad()
#
#
# @pytest.fixture
# def builder(pad, build_path):
#     yield Builder(pad, build_path)
#
#
# @pytest.fixture
# def F():
#     from lektor.db import F
#
#     return F
#
#
# @pytest.fixture
# def web_ui(tmpdir, env):
#     yield WebUI(env, output_path=str(tmpdir))
