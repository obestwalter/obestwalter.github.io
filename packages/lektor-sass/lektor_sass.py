import logging
import subprocess
import time

from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class SassPlugin(Plugin):
    name = "Lektor Sass"
    description = "Watch sass files and transpile them on changes."
    sassSpec = "_style/style.sass:assets/static/style.css"
    pgrepWatcher = ["pgrep", "-f", sassSpec]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sassPath = "sass"
        log.info(f"Sass path: {self.sassPath}")

    def run_sass(self, watch=True):
        if self.sassProcesses:
            log.info("runs at %s nothing to do" % (self.sassProcesses))
            return

        args = [
            self.sassPath,
            "--no-cache",
            "--watch" if watch else "--update",
            self.sassSpec,
        ]
        log.info(f"spawn: %s", " ".join(args))
        subprocess.Popen(args, cwd=self.env.root_path)

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get("sass"))

    def on_server_spawn(self, **extra):
        flags = extra.get("extra_flags") or extra.get("build_flags") or {}
        if not self.is_enabled(flags):
            return

        self.run_sass()

    def on_server_stop(self, **_):
        processes = self.sassProcesses
        if processes:
            for pid in processes:
                subprocess.check_call(["kill", pid])

    def on_before_build_all(self, builder, **_):
        flags = getattr(builder, "extra_flags", getattr(builder, "build_flags", None))
        if not self.is_enabled(flags) or self.sassProcesses:
            return

        log.info("starting sass build")
        self.run_sass(watch=False)
        while self.sassProcesses:
            log.info("wait for sass build")
            time.sleep(0.5)
        log.info("sass build finished")

    @property
    def sassProcesses(self):
        try:
            out = subprocess.check_output(self.pgrepWatcher).decode().strip()
            return out.split("\n")
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return
