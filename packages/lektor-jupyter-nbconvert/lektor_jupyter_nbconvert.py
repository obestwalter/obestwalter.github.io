import logging

from lebut import ipynb_to_md, PATH
from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class JupyterNbConvertPlugin(Plugin):
    name = "Lektor Jupyter Nbconvert"
    description = "Convert changed .ipynb to .lr on server spawn."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.info(f"initialized '{self.name}'")

    def on_server_spawn(self, **_):
        ipynb_to_md.process_all(PATH.ARTICLES)

    def on_before_build(self, source, **_):
        if source.path and "ipynb" in source.path:
            log.info(f"working with {source}")
            ipynb_to_md.process(PATH.CONTENT, PATH.CONTENT / source.path[1:])


if __name__ == "__main__":
    import lektor.pluginsystem

    logging.basicConfig(level=logging.DEBUG)
    lektor.pluginsystem.weakref = lambda x: x
    jp = JupyterNbConvertPlugin(None, "some-id")
    jp.on_server_spawn()
