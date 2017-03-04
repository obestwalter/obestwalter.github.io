from collections import namedtuple

from markupsafe import Markup

from lektor.pluginsystem import Plugin
from lektor.utils import slugify

TocEntry = namedtuple('TocEntry', ['anchor', 'title', 'children'])


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = 'Markdown Header Anchors'
    description = 'Adds anchors to markdown headers.'

    def on_markdown_config(self, config, **_):
        class HeaderAnchorMixin(object):
            def header(renderer, text, level, raw):
                a = slugify(raw)
                p = '<a class="header-anchor" href="#%s">&para;</a>' % (a)
                h = '<h%d id="%s">%s %s</h%d>' % (level, a, text, p, level)
                # noinspection PyUnresolvedReferences
                renderer.meta['toc'].append((level, a, Markup(text)))
                return h
        config.renderer_mixins.append(HeaderAnchorMixin)

    def on_markdown_meta_init(self, meta, **_):
        meta['toc'] = []

    def on_markdown_meta_postprocess(self, meta, **_):
        prev_level = None
        toc = []
        stack = [toc]
        for level, anchor, title in meta['toc']:
            if prev_level is None:
                prev_level = level
            elif prev_level == level - 1:
                stack.append(stack[-1][-1][2])
                prev_level = level
            elif prev_level > level:
                while prev_level > level:
                    # Just a simple workaround for when people do weird
                    # shit with headlines.
                    if len(stack) > 1:
                        stack.pop()
                    prev_level -= 1
            stack[-1].append(TocEntry(anchor, title, []))
        meta['toc'] = toc
