import atexit
import logging
import shutil
import subprocess
import time

from lebut.config import PATH
from lektor.cli import Context
from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class SassPlugin(Plugin):
    name = "Lektor Sass"
    description = "Watch sass files and transpile them on changes."
    SPEC = "_style/style.sass:assets/static/style.css"

    def start_sass_process(self, watch: bool):
        if self.sassProcesses:
            log.info("nothing to do - sass is running")
            return

        args = ["sass", "--no-cache", "--watch" if watch else "--update", self.SPEC]
        log.info("spawn: %s", " ".join(args))
        subprocess.Popen(args, cwd=self.env.root_path)
        while not self.sassProcesses:
            log.info("wait for sass process to spawn")
            time.sleep(0.5)

    def on_before_build_all(self, **_):
        atexit.register(self._kill_all_sass)  # in case server stop is not emitted
        self.start_sass_process(watch=True)

    @property
    def sassProcesses(self):
        cmd = ["pgrep", "-f", self.SPEC]
        try:
            out = subprocess.check_output(cmd).decode().strip()
            return out.split("\n")
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return

    def _kill_all_sass(self):
        processes = self.sassProcesses
        if processes:
            for pid in processes:
                subprocess.check_call(["kill", pid])


def watch_and_deploy_manually():
    logging.basicConfig(level=logging.DEBUG)
    plugin = SassPlugin(Context().get_env(), "sass")
    plugin.on_before_build_all()
    while True:
        shutil.copy(
            str(PATH.PROJECT / "assets" / "static" / "style.css"),
            str(PATH.OUTPUT / "static" / "style.css"),
        )
        log.info("deployed style.css")
        time.sleep(1)


if __name__ == "__main__":
    watch_and_deploy_manually()
