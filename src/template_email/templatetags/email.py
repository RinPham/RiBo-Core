from django.template import Library, Node
from ribo_api.services.utils import Utils

register = Library()


def do_email_tag(parser, token):
    tag = token.contents
    nodelist = parser.parse(('end%s' % tag,))
    parser.delete_first_token()
    return EmailNode(tag, nodelist)


class EmailNode(Node):
    def __init__(self, tag, nodelist):
        self.tag = tag
        self.nodelist = nodelist

    def render(self, context):
        context_var = '_%s' % self.tag
        if not context.get(context_var, False):
            return ''
        return self.nodelist.render(context)


def gen_loc_slug(loc, arg=None):
    return Utils.gen_search_slug('', loc.display_text)


register.filter('gen_loc_slug', gen_loc_slug)
register.tag('subject', do_email_tag)
register.tag('body', do_email_tag)
register.tag('bodyhtml', do_email_tag)

css = [
    'background-color: #0090de; border: solid 2px #A0DEFF;',
    'background-color: #845bf0; border: solid 2px #CAB6FF;',
    'background-color: #5fc67c; border: solid 2px #8DF7AA;',
    'background-color: #efa23d; border: solid 2px #FFC77F;',
    'background-color: #ea5d5d; border: solid 2px #FFD2D2;',
]


@register.filter(name='gid2colorcode')
def gid2colorcode(value):
    index = value % 5;
    style = '" style="width: 38px; height: 38px; vertical-align: middle; text-align: center; border-radius: 50%;'
    style += css[index]
    return style
