from lektor.pluginsystem import Plugin


# todo keep count
class FootnotyMixin:
    """Creates numbered footnotes from named markers and links them to their
    corresponding named footnotes.

    e.g. My super deep thought#(DNA)#.

    #(DNA)# In HHGTTG DNA said ... bla bla bla

    Turns into

    My super deep thought[1].

    [1] In HHGTTG DNA said ... bla bla bla
    """
    # TODO keep something here to remember the current footnote count?

    # # find a generic footnote marker and remember the number
    # REF_RE = re.compile(r'???')
    # # grab whole footnote section and split into single footnotes
    # NOTE_RE = re.compile(r'???')

    def paragraph(self, text):
        return super().paragraph(text)
        #
        # refMatch = self.REF_RE.match(text)
        # # todo cache -> is only needed to be grabbed once per file
        # noteMatch = self.NOTE_RE.match(text)
        #
        # # TODO this is still basically the old plugin
        # if refMatch is None:
        #     return super().paragraph(text)
        # Number = len(ref.group(1))
        # return '<div class="admonition admonition-%s"><p>%s</p></div>' % (
        #     CLASSES[Number],
        #     text[ref.end():]
        # )


class Footnoty(Plugin):
    name = u'Create footnotes and their back links'
    description = u'Adds admonitions to markdown.'

    def on_markdown_config(self, config, **extra):
        config.renderer_mixins.append(FootnotyMixin)
