import logging

from lebut.compile_notebooks import JupyterNbConvert
from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class JupyterNbConvertPlugin(Plugin):
    name = "Lektor Jupyter Nbconvert"
    description = "Convert changed .ipynb to .lr files before lektor build starts."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = JupyterNbConvert()
        log.info(f"initialized '{self.name}'")

    def on_before_build_all(self, **_):
        # FIXME this is being triggered all the time, WHY?
        log.info("compile ipynb files")
        self._instance.convert()


if __name__ == "__main__":
    import lektor.pluginsystem

    logging.basicConfig(level=logging.DEBUG)
    lektor.pluginsystem.weakref = lambda x: x
    jp = JupyterNbConvertPlugin(None, "some-id")
    jp.on_before_build_all()
