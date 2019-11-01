import logging
import re

from mistune import escape
from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class MarkdownCustomizePlugin(Plugin):
    name = "Lektor Markdown Customize"
    description = "Massage the markdown renderer before rendering."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.info(f"initialized: {self.name}")

    def on_markdown_config(self, config, **_):
        config.renderer_mixins.append(FootnoteRepairMixin)

    # def on_markdown_lexer_config(
    #     self, config: MarkdownConfig, renderer: ImprovedRenderer
    # ):
    #     print(config)
    #     print(renderer)


class FootnoteRepairMixin:
    def footnote_ref(self, key, index):
        html = (
            '<sup class="footnote-ref" id="fnref-%s">'
            '<a href="#fn-%s">&thinsp;[%d]</a></sup>'
        ) % (escape(key), escape(key), index)
        return html

    def footnote_item(self, key, text):
        back = ('<a href="#fnref-%s" class="footnote"> [&#10548;]</a>') % escape(key)
        text = text.rstrip()
        if text.endswith("</p>"):
            text = re.sub(r"<\/p>$", r"%s</p>" % back, text)
        else:
            text = "%s<p>%s</p>" % (text, back)
        html = '<li id="fn-%s">%s</li>\n' % (escape(key), text)
        return html
