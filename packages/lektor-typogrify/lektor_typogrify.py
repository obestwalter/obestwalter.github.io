from markupsafe import Markup
from typogrify.filters import typogrify

from lektor.markdown import Markdown
from lektor.pluginsystem import Plugin


class TypogrifyPlugin(Plugin):
    name = 'Lektor Typogrify'
    description = 'Add filter to jinja environment.'

    @staticmethod
    def _typogrify(markdown: Markdown):
        return Markup(typogrify(str(markdown.html)))

    def on_setup_env(self, **_):
        self.env.jinja_env.filters['typogrify'] = self._typogrify
