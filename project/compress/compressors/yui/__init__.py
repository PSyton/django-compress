from compress.conf import settings
from compress.compressors import SubProcessCompressor

class YUICompressor(SubProcessCompressor):
  def __init__(self, content_type, arguments, verbose):
    self.content_type = content_type
    self.arguments = arguments
    SubProcessCompressor.__init__(self, verbose)

  def compress(self, content):
    command = '%s --type=%s %s' % (settings.COMPRESS_YUI_BINARY, self.content_type, self.arguments)
    if self.verbose:
      command += ' --verbose'
    return self.execute_command(command, content)

class JSYUICompressor(YUICompressor):
  def __init__(self, verbose):
    YUICompressor.__init__(self, content_type = 'js', arguments = settings.COMPRESS_YUI_JS_ARGUMENTS, verbose = verbose )

class CSSYUICompressor(YUICompressor):
  def __init__(self, verbose):
    YUICompressor.__init__(self, content_type = 'css', arguments = settings.COMPRESS_YUI_CSS_ARGUMENTS, verbose = verbose )
