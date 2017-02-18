""" for exploring lektor internally """
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


if __name__ == '__main__':
    _project = Project.discover()
    _env = _project.make_env()
    _pad = _env.new_pad()
    queries(_pad)
