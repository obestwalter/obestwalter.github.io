import os
from string import Template

from pathtools import path

HERE = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(HERE, '..', 'content')
BLUEPRINTS_PATH = os.path.join(HERE, 'blueprints')
TYPE_DST_MAP = {
    'art': os.path.join(CONTENT_PATH, 'articles'),
    'pro': os.path.join(CONTENT_PATH, 'projects'),
    'log': os.path.join(CONTENT_PATH, 'log'),
}


def main(what):
    dstPath = TYPE_DST_MAP[what]

if __name__ == '__main__':
    main('art')
