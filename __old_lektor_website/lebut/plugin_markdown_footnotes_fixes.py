import logging
import re

from mistune import escape

from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class FootnotesFixesPlugin(Plugin):
    name = "Lektor Footnotes Fixes"
    description = "Customize footnotes handling of mistune renderer"

    def on_markdown_config(self, config, **_):  # noqa
        config.renderer_mixins.append(FootnoteRendererMixin)


class FootnoteRendererMixin:
    """Override mistune.Renderer methods to make nicer footnotes."""

    def footnotes(self, text):  # noqa
        return f'<div class="footnotes">\n<ol>{text}</ol>\n</div>\n'

    def footnote_ref(self, key, index):  # noqa
        key = escape(key)
        html = (
            f'<sup class="footnote-ref" id="fnref-{key}">'
            f'<a href="#fn-{key}">&thinsp;[{index:d}]</a></sup>'
        )
        return html

    def footnote_item(self, key, text):  # noqa
        key = escape(key)
        back = f'<a href="#fnref-{key}" class="footnote"> [&#10548;]</a>'
        text = text.rstrip()
        if text.endswith("</p>"):
            text = re.sub(r"<\/p>$", r"%s</p>" % back, text)
        else:
            text = f"{text}<p>{back}</p>"
        html = f'<li id="fn-{key}">{text}</li>\n'
        return html
