# -*- coding: utf-8 -*-
import os
import subprocess

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
from lektor.utils import portable_popen


class SassPlugin(Plugin):
    name = u'lektor-sass'
    description = u'Watch sass files and transpile them on changes.'
    rubyPathCmd = ["ruby", "-rubygems", "-e", "puts Gem.user_dir"]

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.sass_process = None
        rubyPath = subprocess.check_output(self.rubyPathCmd).decode().strip()
        self.sassPath = os.path.join(rubyPath, 'bin', 'sass')
        reporter.report_generic('Sass path: %s' % self.sassPath)

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get('sass'))

    def run_sass(self, watch=False):
        args = [self.sassPath, '--no-cache']
        if watch:
            args.append('--watch')
        args.append('assets/static')
        return portable_popen(args, cwd=self.env.root_path)

    def on_server_spawn(self, **extra):
        extra_flags = (
            extra.get("extra_flags") or extra.get("build_flags") or {})
        if not self.is_enabled(extra_flags):
            return

        reporter.report_generic('Spawning sass watcher')
        self.sass_process = self.run_sass(watch=True)

    # noinspection PyUnusedLocal
    def on_server_stop(self, **extra):
        if self.sass_process is not None:
            reporter.report_generic('Stopping sass watcher')
            self.sass_process.kill()

    # noinspection PyUnusedLocal
    def on_before_build_all(self, builder, **extra):
        extra_flags = getattr(
            builder, "extra_flags", getattr(builder, "build_flags", None)
        )
        if not self.is_enabled(extra_flags) \
           or self.sass_process is not None:
            return
        self.npm_install()
        reporter.report_generic('Starting sass build')
        self.run_sass().wait()
        reporter.report_generic('Sass build finished')
