import logging
import os
import subprocess
import time

from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class SassPlugin(Plugin):
    name = 'Lektor Sass'
    description = 'Watch sass files and transpile them on changes.'
    rubyPathCmd = ["ruby", "-rubygems", "-e", "puts Gem.user_dir"]
    sassSpec = 'assets/static:assets/static'
    pgrepWatcher = ['pgrep', '-f', sassSpec]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rubyBin = subprocess.check_output(self.rubyPathCmd).decode().strip()
        self.sassPath = os.path.join(rubyBin, 'bin', 'sass')
        log.info('Sass path: %s' % self.sassPath)

    def run_sass(self, watch=True):
        if self.sassPid:
            log.info("already running - nothing to do (%s)" % (self.sassPid))
            return

        args = [self.sassPath, '--no-cache',
                '--watch' if watch else '--update',
                self.sassSpec]
        subprocess.Popen(args, cwd=self.env.root_path)

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get('sass'))

    def on_server_spawn(self, **extra):
        flags = extra.get("extra_flags") or extra.get("build_flags") or {}
        if not self.is_enabled(flags):
            return

        log.info('Spawning sass watcher')
        self.run_sass()

    def on_server_stop(self, **_):
        pids = self.sassPid
        if pids:
            subprocess.check_call(['kill'] + pids)

    def on_before_build_all(self, builder, **_):
        flags = getattr(
            builder, "extra_flags", getattr(builder, "build_flags", None))
        if not self.is_enabled(flags) or self.sassPid:
            return

        log.info('Starting sass build')
        self.run_sass(watch=False)
        while self.sassPid:
            log.info("wait for sass build")
            time.sleep(1)
        log.info('Sass build finished')

    @property
    def sassPid(self):
        try:
            out = subprocess.check_output(self.pgrepWatcher).decode().strip()
            return out.split('\n')
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return
