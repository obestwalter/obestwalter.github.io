import os
from io import BytesIO

from lektor.admin.modules import serve
from lektor.cli import Context
from lektor.devserver import run_server

# I don't use the editor - get rid of the button during development
serve.rewrite_html_for_editing = lambda fp, edit_url: BytesIO(fp.read())


class MyLektor(object):
    here = os.path.dirname(__file__)
    outputPath = os.path.join(here, '..', '..', 'website_build')
    rubyPathCmd = ["ruby", "-rubygems", "-e", "puts Gem.user_dir"]

    def __init__(self):
        self.ctx = Context()
        self.ctx.load_plugins()
        self.env = self.ctx.get_env()
        print(' * Project path: %s' % self.ctx.get_project().project_path)
        print(' * Output path: %s' % self.outputPath)

    def run(self):
        self.run_server()

    def run_server(self):
        run_server(
            ('0.0.0.0', 8080),
            self.env,
            self.outputPath,
            verbosity=0,  # 0 -4
            lektor_dev=False,
            browse=True,
            prune=True,
            extra_flags=['sass'],
            ui_lang=self.ctx.ui_lang,
        )


def main():
    MyLektor().run()

if __name__ == '__main__':
    main()
