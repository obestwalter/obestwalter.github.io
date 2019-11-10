import logging
import subprocess
import time

from lebut.config import PATH

log = logging.getLogger(__name__)


class LiveReloader:
    cmd = "livereload"

    def start_with_keep_alive(self, **_):
        self.start()
        while self._is_alive:
            log.info("livereload is active")
            time.sleep(10)

    def start(self):
        if self._is_alive:
            log.info(f"nothing to do - {self.cmd} is running")
            return

        args = [self.cmd, "--host", "0.0.0.0", "--port", "8080", str(PATH.OUTPUT)]
        log.info("spawn: %s", " ".join(args))
        subprocess.Popen(args)
        while not self._is_alive:
            log.info(f"wait for {self.cmd} process to spawn")
            time.sleep(0.5)

    @property
    def _is_alive(self):
        cmd = ["pgrep", "-af", "livereload"]
        try:
            out = subprocess.check_output(cmd).decode().strip()
            return out.split("\n")
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    lr = LiveReloader()
    lr.start_with_keep_alive()
