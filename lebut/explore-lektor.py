"""Some little functions to help exploring lektor internals interactively."""
from lektor.db import Query
from lektor.project import Project


def queries(pad):
    q = Query('/articles', pad).order_by('-mtime')
    for e in q:
        print(e)


def children(pad):
    root_record = pad.root
    print(root_record)
    for c in root_record.children:
        print(c)


def explore_pad():
    _project = Project.discover()
    _env = _project.make_env()
    _pad = _env.new_pad()
    queries(_pad)


if __name__ == '__main__':
    from lebut.cli import Workflow

    Workflow.serve()