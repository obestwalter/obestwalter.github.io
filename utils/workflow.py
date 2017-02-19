"""
Helpers for my workflow.

    draft art "My super article"

creates a prepared md file with all the necessary settings to work on.

    publish drafts/art-my-super-article.md

will make the necessary adjustments and publish it in the contents.
"""
import os
import subprocess
from datetime import datetime
from string import Template

import sys
from lektor.utils import slugify

_HERE = os.path.dirname(__file__)
BLUEPRINTS_PATH = os.path.join(_HERE, 'blueprints')
PROJECT_PATH = os.path.join(_HERE, '..')
DRAFTS_PATH = os.path.join(PROJECT_PATH, 'drafts')
CONTENT_PATH = os.path.join(PROJECT_PATH, 'content')

ARTICLE = 'art'
DIARY = 'dia'
KINDS = [ARTICLE, DIARY]
KIND_DST_MAP = {
    ARTICLE: os.path.join(CONTENT_PATH, 'articles'),
    DIARY: os.path.join(CONTENT_PATH, 'diary'),
}


def draft():
    kind, title = sys.argv[1:3]
    assert kind in KINDS, kind
    with open(os.path.join(BLUEPRINTS_PATH, '%s.md' % kind)) as f:
        content = f.read()
    rep = dict(title=title)
    content = Template(content).safe_substitute(rep)
    dst = os.path.join(DRAFTS_PATH, '%s-%s.md' % (kind, slugify(title)))
    assert not os.path.exists(dst), dst
    with open(dst, 'w') as f:
        f.write(content)


def publish():
    path = sys.argv[1]
    with open(os.path.join(PROJECT_PATH, path)) as f:
        content = f.read()
    rep = dict(date=datetime.now().strftime('%Y-%m-%d'))
    content = Template(content).safe_substitute(rep)
    name = os.path.splitext(os.path.basename(path))[0]
    kind, name = name.split('-', 1)
    dst = os.path.join(KIND_DST_MAP[kind], name, 'contents.lr')
    os.mkdir(os.path.dirname(dst))
    with open(dst, 'w') as f:
        f.write(content)
    os.remove(path)


def deploy():
    # print(subprocess.check_output(["lektor",  "clean", "--yes"]))
    print(subprocess.check_output(["lektor", "build"]))
    print(subprocess.check_output(["lektor", "deploy"]))
