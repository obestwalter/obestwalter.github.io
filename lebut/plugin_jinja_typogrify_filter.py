import logging

from markupsafe import Markup
from typogrify.filters import typogrify

from lektor.markdown import Markdown
from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class JinjaTypogrifyFilterPlugin(Plugin):
    name = "Jinja Typogrify Filter Plugin"
    description = "Add typogrify filter"

    def on_setup_env(self, **_):
        self.env.jinja_env.filters["typogrify"] = self.jinja_typogrify_filter

    @staticmethod
    def jinja_typogrify_filter(markdown: Markdown):
        return Markup(typogrify(str(markdown.html)))
