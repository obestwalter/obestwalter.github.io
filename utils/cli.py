import os
import subprocess
import sys
from datetime import datetime
from io import BytesIO
from string import Template

import fire

from lektor.cli import Context
from lektor.devserver import run_server
from lektor.reporter import reporter
from lektor.utils import slugify

# I don't use the editor - get rid of the button during development
run_server.rewrite_html_for_editing = lambda fp, edit_url: BytesIO(fp.read())

HERE = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(HERE, '..')
DRAFTS_PATH = os.path.join(PROJECT_PATH, 'drafts')
ARTICLES_PATH = os.path.join(PROJECT_PATH, 'content', 'articles')


class CLI:
    @classmethod
    def serve(cls):
        here = os.path.dirname(__file__)
        outputPath = os.path.join(here, '..', '..', 'website_build')
        ctx = Context()
        ctx.load_plugins()
        env = ctx.get_env()
        print(' * Project path: %s' % ctx.get_project().project_path)
        print(' * Output path: %s' % outputPath)

        run_server(
            ('0.0.0.0', 8080),
            env,
            outputPath,
            verbosity=0,  # 0 -4
            lektor_dev=False,
            browse=True,
            prune=True,
            extra_flags=['sass'],
            ui_lang=ctx.ui_lang,
        )

    @classmethod
    def draft(cls):
        title = sys.argv[1]
        with open(os.path.join(HERE, 'article-blueprint.md')) as f:
            content = f.read()
        rep = dict(title=title)
        content = Template(content).safe_substitute(rep)
        dst = os.path.join(DRAFTS_PATH, '%s.md' % slugify(title))
        assert not os.path.exists(dst), dst
        with open(dst, 'w') as f:
            f.write(content)

    @classmethod
    def publish(cls):
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

    @classmethod
    def deploy(cls):
        if len(sys.argv) > 2 and sys.argv[2] == 'clean':
            first = subprocess.check_output(['lektor', 'clean', '--yes'])
        else:
            first = subprocess.check_output(['lektor', 'build'])
        second = subprocess.check_output(['lektor', 'deploy'])
        reporter.report_generic(first.decode() + '\n' + second.decode())


def main():
    fire.Fire(CLI)
