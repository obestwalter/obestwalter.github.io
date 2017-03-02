import os
import subprocess

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter


class SassPlugin(Plugin):
    name = 'Lektor Sass'
    description = 'Watch sass files and transpile them on changes.'
    rubyPathCmd = ["ruby", "-rubygems", "-e", "puts Gem.user_dir"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sassProcess = None
        rubyBin = subprocess.check_output(self.rubyPathCmd).decode().strip()
        self.sassPath = os.path.join(rubyBin, 'bin', 'sass')
        reporter.report_generic('Sass path: %s' % self.sassPath)

    def run_sass(self, watch=True):
        args = [self.sassPath, '--no-cache']
        if watch:
            args.append('--watch')
        args.append('assets/static')
        return subprocess.Popen(args, cwd=self.env.root_path)

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get('sass'))

    def on_server_spawn(self, **extra):
        flags = extra.get("extra_flags") or extra.get("build_flags") or {}
        if not self.is_enabled(flags):
            return

        reporter.report_generic('Spawning sass watcher')
        self.sassProcess = self.run_sass()

    def on_server_stop(self, **_):
        if self.sassProcess:
            reporter.report_generic('Stopping sass watcher')
            self.sassProcess.kill()

    def on_before_build_all(self, builder, **_):
        flags = getattr(
            builder, "extra_flags", getattr(builder, "build_flags", None))
        if not self.is_enabled(flags) or self.sassProcess is not None:
            return

        reporter.report_generic('Starting sass build')
        self.run_sass(watch=False).wait()
        reporter.report_generic('Sass build finished')
