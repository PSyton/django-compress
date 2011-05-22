from django import template
from django.template.loader import render_to_string

from compress.conf import settings
from compress.packager import Packager, PackageNotFound

register = template.Library()

class CompressedNode(template.Node):
  def __init__(self, name, aType):
    self.name = name
    self.type = aType
    if aType == 'css':
      self.template = "compress/css.html"
    else:
      self.template = "compress/js.html"
    self.packager = Packager()

  def create_tags(self, package, path):
     context = {}
     if 'context' in package:
       context = package['context']
     context.update({
       'url': self.packager.individual_url( path )
     })
     return render_to_string(package['template'], context)

  def render(self, context):
    package_name = template.Variable(self.name).resolve(context)
    try:
      package = self.packager.package_for(self.type ,package_name)
      package['type'] = self.type

    except PackageNotFound:
      return ''  # fail silently, do not return anything if an invalid group is specified

    if not 'template' in package:
      package['template'] = self.template

    if 'externals' in package:
      out = '\n'.join([self.render_external(package, url) for url in package['externals']])
    else:
      out = ''

    if settings.COMPRESS:
      compressed_path = self.packager.pack( package )
      out += self.create_tags(package, compressed_path)
    else:
      package['paths'] = self.packager.compile(package['paths'])
      out += self.render_individual(package)

    return out

  def render_external(self, package, url):
    return render_to_string(package['template'], { 'url': url })

  def render_individual(self, package):
    tags = [self.create_tags(package, path) for path in package['paths']]
    return '\n'.join(tags)

def compressed_css(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the COMPRESS_CSS setting' % token.split_contents()[0]

    return CompressedNode( name, 'css' )
compressed_css = register.tag(compressed_css)


def compressed_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the COMPRESS_JS setting' % token.split_contents()[0]
    return CompressedNode( name, 'js' )
compressed_js = register.tag(compressed_js)
