import logging
import re

from lektor.pluginsystem import Plugin

log = logging.getLogger(__name__)


class MarkdownAdmonitionsPlugin(Plugin):
    name = "Markdown Admonition"
    description = "Add admonitions"

    def on_markdown_config(self, config, **_):  # noqa
        config.renderer_mixins.append(AdmonitionRendererMixin)


class AdmonitionRendererMixin:
    """Filched from https://github.com/lektor/lektor-markdown-admonition

    !     -> <div class="admonition admonition-note">
    !!    -> <div class="admonition admonition-info">
    !!!   -> <div class="admonition admonition-tip">
    !!!!  -> <div class="admonition admonition-warning">
    !!!!!  -> <div class="admonition admonition-tldr">
    """

    REGEX = re.compile(r"^\s*(!{1,5})\s+")
    CLASSES = {1: "note", 2: "info", 3: "tip", 4: "warning", 5: "TLDR"}

    def paragraph(self, text):
        match = self.REGEX.match(text)
        if match is None:
            # noinspection PyUnresolvedReferences
            return super().paragraph(text)

        level = len(match.group(1))
        return (
            f'<div class="admonition-{self.CLASSES[level]}">'
            f"<p>{text[match.end():]}</p></div>"
        )
