import web, os
from web.contrib.template import render_mako

def getit (self, name):
    # Assuming all templates are mako
    path = name + ".mako"
    t = self._lookup.get_template(path)
    web.header('Content-Type','text/html; charset=utf-8')
    return t.render

web.contrib.template.render_mako.__getattr__ = getit

render = render_mako(
    directories=[os.path.dirname(__file__)],
    input_encoding='utf-8',
    output_encoding='utf-8',
)