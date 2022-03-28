import logging

from lebut.config import LEBUT
from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class JinjaEnvInjector(Plugin):
    name = "Jinja Env Injector"
    description = "Inject variables into global template namespace"

    def on_setup_env(self, **_):
        self.env.jinja_env.globals['LEBUT'] = LEBUT
