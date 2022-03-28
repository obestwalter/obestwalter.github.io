import logging

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class PygmentsRendererPlugin(Plugin):
    name = "Pygments Renderer Plugin"
    description = "Add code highlighting for markdown"

    def on_markdown_config(self, config, **_):  # noqa
        config.renderer_mixins.append(PygmentsRendererMixin)


class PygmentsRendererMixin:
    """Filched from https://github.com/lektor/lektor-markdown-highlighter"""

    def block_code(self, code, lang):
        if not lang:
            # noinspection PyUnresolvedReferences
            return super().block_code(code, lang)
        lexer = get_lexer_by_name(lang)
        # TODO figure out if I have to pass a style at all (I don't use it)
        # TODO figure out if it is necessary to create a new instance each time
        formatter = HtmlFormatter(style="default")
        return highlight(code, lexer, formatter)
