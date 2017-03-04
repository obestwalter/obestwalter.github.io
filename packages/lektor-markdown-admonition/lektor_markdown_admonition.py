import re

from lektor.pluginsystem import Plugin


class AdmonitionMixin:
    REGEX = re.compile(r'^\s*(!{1,4})\s+')
    CLASSES = {
        1: 'note',
        2: 'info',
        3: 'tip',
        4: 'warning'}

    def paragraph(self, text):
        match = self.REGEX.match(text)
        if match is None:
            # noinspection PyUnresolvedReferences
            return super().paragraph(text)

        level = len(match.group(1))
        return '<div class="admonition-%s"><p>%s</p></div>' % (
            self.CLASSES[level], text[match.end():])


class MarkdownAdmonitionPlugin(Plugin):
    name = u'Markdown Admonition'
    description = u'Adds admonitions to markdown.'

    def on_markdown_config(self, config, **_):
        config.renderer_mixins.append(AdmonitionMixin)
