"""Filched from https://github.com/lektor/lektor-markdown-header-anchors"""
from slugify import slugify

from lektor.pluginsystem import Plugin
import uuid
from markupsafe import Markup
from collections import namedtuple


TocEntry = namedtuple("TocEntry", ["anchor", "title", "children"])


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = "Markdown Header Anchors"
    description = (
        u"Lektor plugin that adds anchors and table of contents to markdown headers."
    )

    def on_markdown_config(self, config, **_):
        class HeaderAnchorMixin(object):
            def header(renderer, text, level, raw):  # noqa
                if self.get_config().get("anchor-type") == "random":
                    a = uuid.uuid4().hex[:6]
                else:
                    a = slugify(raw)
                renderer.meta["toc"].append((level, a, Markup(text)))  # noqa
                p = f'<a class="header-anchor" href="#{a}">&#128279;</a>'  # or &para;
                h = f'<h{level} id="{a}">{text} {p}</h{level}>'
                return h

        config.renderer_mixins.append(HeaderAnchorMixin)

    def on_markdown_meta_init(self, meta, **_):  # noqa
        meta["toc"] = []

    def on_markdown_meta_postprocess(self, meta, **_):  # noqa
        prev_level = None
        toc = []
        stack = [toc]

        for level, anchor, title in meta["toc"]:
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

        meta["toc"] = toc
