from __future__ import print_function

import os
import sys
from io import BytesIO

from lektor.admin.modules import serve
from lektor.cli import Context
from lektor.devserver import run_server

# I don't use the editor - get rid of the button during development
serve.rewrite_html_for_editing = lambda fp, edit_url: BytesIO(fp.read())


def main():
    ctx = Context()
    ctx.load_plugins()
    here = os.path.dirname(__file__)
    outputPath = os.path.join(here, '..', '..', 'website_build')
    print(' * Project path: %s' % ctx.get_project().project_path)
    print(' * Output path: %s' % outputPath)
    run_server(
        ('0.0.0.0', '8080'),
        ctx.get_env(),
        outputPath,
        verbosity=0,  # 0 -4
        lektor_dev=False,
        browse=True,
        prune=True,
        extra_flags=None,  # from plugins - e.g. webpack
        ui_lang=ctx.ui_lang,
    )

if __name__ == '__main__':
    sys.exit(main())
