from typogrify.filters import typogrify

from lektor.pluginsystem import Plugin


class TypogrifyPlugin(Plugin):
    name = 'Lektor Typogrify'
    description = 'Add filter to jinja environment.'

    @staticmethod
    def _typogrify(value):
        return typogrify(str(value))

    def on_setup_env(self, **_):
        self.env.jinja_env.filters['typogrify'] = typogrify
