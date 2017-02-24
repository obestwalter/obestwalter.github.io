"""
Helpers for my evolving workflow.

    draft [art] "My super article"

creates a prepared md file with all the necessary settings to work on.

    publish drafts/my-super-article.md

will make the necessary adjustments and publish it in the contents.

    deploy [clean]

will create a [clean] build and push it online.
"""
from __future__ import print_function

import os
import subprocess
import sys
from datetime import datetime
from string import Template

from lektor.utils import slugify

HERE = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(HERE, '..')
DRAFTS_PATH = os.path.join(PROJECT_PATH, 'drafts')
CONTENT_PATH = os.path.join(PROJECT_PATH, 'content')


def draft():
    title = sys.argv[1]
    with open(os.path.join(HERE, 'article-blueprint.md')) as f:
        content = f.read()
    rep = dict(title=title)
    content = Template(content).safe_substitute(rep)
    dst = os.path.join(DRAFTS_PATH, '%s.md' % slugify(title))
    assert not os.path.exists(dst), dst
    with open(dst, 'w') as f:
        f.write(content)


def publish():
    srcPath = sys.argv[1]
    with open(srcPath) as f:
        content = f.read()
    rep = dict(date=datetime.now().strftime('%Y-%m-%d'))
    content = Template(content).safe_substitute(rep)
    slug = os.path.splitext(os.path.basename(srcPath))[0]
    containerPath = os.path.join(CONTENT_PATH, slug)
    assert not os.path.exists(containerPath), containerPath
    os.mkdir(containerPath)
    dst = os.path.join(containerPath, 'contents.lr')
    with open(dst, 'w') as f:
        f.write(content)
    os.remove(srcPath)


def deploy():
    if len(sys.argv) > 2 and sys.argv[2] == 'clean':
        print(subprocess.check_output(['lektor',  'clean', '--yes']))
    else:
        print(subprocess.check_output(['lektor', 'build']))
    print(subprocess.check_output(['lektor', 'deploy']))
