import os
from string import Template
from datetime import datetime

from lektor.utils import slugify

HERE = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(HERE, '..', 'content')
BLUEPRINTS_PATH = os.path.join(HERE, 'blueprints')
TYPE_DST_MAP = {
    'art': os.path.join(CONTENT_PATH, 'articles'),
    'dia': os.path.join(CONTENT_PATH, 'diary'),
}


def main(what, title):
    with open(os.path.join(BLUEPRINTS_PATH, "%s.lr" % what)) as f:
        content = f.read()
    rep = dict(title=title, date=datetime.now().strftime("%Y-%m-%d"))
    content = Template(content).substitute(rep)
    dst = os.path.join(TYPE_DST_MAP[what], slugify(title), "contents.lr")
    with open(dst, "w") as f:
        f.write(content)


if __name__ == '__main__':
    main('art', "My super title")
