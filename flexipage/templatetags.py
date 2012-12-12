from django import template

def flexi_content(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, content_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (content_name[0] == content_name[-1] and content_name[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return CurrentTimeNode(format_string[1:-1])



