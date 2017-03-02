import os
import subprocess
import sys
from datetime import datetime
from string import Template

from lektor.reporter import reporter
from lektor.utils import slugify

HERE = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(HERE, '..')
DRAFTS_PATH = os.path.join(PROJECT_PATH, 'drafts')
ARTICLES_PATH = os.path.join(PROJECT_PATH, 'content', 'articles')


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
    containerPath = os.path.join(ARTICLES_PATH, slug)
    assert not os.path.exists(containerPath), containerPath
    os.mkdir(containerPath)
    dstPath = os.path.join(containerPath, 'contents.lr')
    with open(dstPath, 'w') as f:
        f.write(content)
    os.remove(srcPath)
    subprocess.check_call(['git', 'add', dstPath])


def deploy():
    if len(sys.argv) > 2 and sys.argv[2] == 'clean':
        first = subprocess.check_output(['lektor',  'clean', '--yes'])
    else:
        first = subprocess.check_output(['lektor', 'build'])
    second = subprocess.check_output(['lektor', 'deploy'])
    reporter.report_generic(first.decode() + '\n' + second.decode())
