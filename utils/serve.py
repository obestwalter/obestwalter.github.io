from __future__ import print_function

import os
import subprocess
import sys
from io import BytesIO

from lektor.admin.modules import serve
from lektor.cli import Context
from lektor.devserver import run_server

# I don't use the editor - get rid of the button during development
serve.rewrite_html_for_editing = lambda fp, edit_url: BytesIO(fp.read())


class MyLektor(object):
    here = os.path.dirname(__file__)
    outputPath = os.path.join(here, '..', '..', 'website_build')

    def __init__(self):
        self.ctx = Context()
        self.ctx.load_plugins()
        self.env = self.ctx.get_env()
        rubyPath = subprocess.check_output(
            ["ruby", "-rubygems", "-e", "puts Gem.user_dir"]).strip()
        self.sassPath = os.path.join(rubyPath, 'bin', 'sass')
        print(' * Sass path: %s' % self.sassPath)
        print(' * Project path: %s' % self.ctx.get_project().project_path)
        print(' * Output path: %s' % self.outputPath)

    def run(self):
        self.run_sass()
        self.run_server()

    def run_sass(self):
        args = [self.sassPath, '--no-cache', '--watch', 'assets/static']
        return subprocess.Popen(args, cwd=self.env.root_path)

    def run_server(self):
        run_server(
            ('0.0.0.0', '8080'),
            self.env,
            self.outputPath,
            verbosity=4,  # 0 -4
            lektor_dev=False,
            browse=True,
            prune=True,
            extra_flags=None,
            ui_lang=self.ctx.ui_lang,
        )

if __name__ == '__main__':
    sys.exit(MyLektor().run())
