import logging
import os
import subprocess
from datetime import datetime
from io import BytesIO
from string import Template

from lektor.cli import Context
from lektor.devserver import run_server
from lektor.utils import slugify

# I don't use the editor - get rid of the button during development
run_server.rewrite_html_for_editing = lambda fp, edit_url: BytesIO(fp.read())

HERE = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(HERE, '..')
DRAFTS_PATH = os.path.join(PROJECT_PATH, 'drafts')
ARTICLES_PATH = os.path.join(PROJECT_PATH, 'content', 'articles')

log = logging.getLogger(__name__)


class Workflow:
    """blog creation, adaption, publishing workflow"""
    here = os.path.dirname(__file__)
    outputPath = os.path.join(here, '..', '..', 'website_build')

    @classmethod
    def serve(cls, host='0.0.0.0', port=8080, outputPath=outputPath,
              verbosity=0, dev=True, reinstall=False, browse=False, prune=True,
              flags=('sass',)):
        ctx = Context()
        ctx.load_plugins(reinstall=reinstall)
        env = ctx.get_env()
        log.info('project path: %s' % ctx.get_project().project_path)
        log.info('output path: %s' % outputPath)
        run_server((host, port),
                   env,
                   outputPath,
                   verbosity=verbosity,  # 0 -4
                   lektor_dev=dev,
                   browse=browse,
                   prune=prune,
                   extra_flags=flags,
                   ui_lang=ctx.ui_lang)

    @classmethod
    def draft(cls, title):
        with open(os.path.join(HERE, 'article-blueprint.md')) as f:
            content = f.read()
        rep = dict(title=title)
        content = Template(content).safe_substitute(rep)
        dst = os.path.join(DRAFTS_PATH, '%s.md' % slugify(title))
        assert not os.path.exists(dst), dst
        with open(dst, 'w') as f:
            f.write(content)

    @classmethod
    def publish(cls, srcPath):
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
            log.info("publishing %s:\n\n%s" % (slug, content))
            f.write(content)
        os.remove(srcPath)
        log.info(subprocess.check_call(['git', 'add', dstPath]))

    @classmethod
    def deploy(cls, clean=False):
        if clean:
            first = subprocess.check_output(['lektor', 'clean', '--yes'])
        else:
            first = subprocess.check_output(['lektor', 'build'])
        second = subprocess.check_output(['lektor', 'deploy'])
        log.info(first.decode() + '\n' + second.decode())


def main():
    import fire

    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(Workflow)
