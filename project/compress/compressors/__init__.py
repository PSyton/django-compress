import os
import re
import subprocess
import urlparse

from compress.conf import settings
from compress.storage import storage
from compress.utils import to_class, make_relative_path

URL_DETECTOR = r'url\([\'"]?([^\s)]+\.[a-z]+)[\'"]?\)'

"""
Base compressor class for proccess some content.
Use it for additional compresors, for example tidycss.

"""
class BaseCompressor(object):
    def __init__(self, verbose):
        self.verbose = verbose
    def compress(self, content):
        """
        In child class you mast implement this method.

        content - this is a content to be compressed

        method returns compressed content
        """
        raise NotImplementedError

class BatchCompressor(object):
    def __init__(self, additional_compressors, verbose):
        self.verbose = verbose
        self.extra_compressors = [to_class(compressor) for compressor in additional_compressors]

    def read_file(self, path):
        """Read file content in binary mode"""
        file = storage.open(path, mode='rb')
        content = file.read().decode('utf8')
        file.close()
        return content

    def concatenate(self, paths):
        return '\n'.join([self.read_file(path) for path in paths])

    def compress(self, paths):
        """Process set of files provided by paths."""
        content = self.concatenate( paths )
        for compressor in self.extra_compressors:
           content = getattr(compressor(verbose=self.verbose), 'compress')(content)
        return content

class JSCompressor(BatchCompressor):
    def __init__(self, verbose = False):
        BatchCompressor.__init__( self
                                , additional_compressors = settings.COMPRESS_JS_COMPRESSORS
                                , verbose = verbose )

class CSSCompressor(BatchCompressor):
    def __init__(self, verbose = False):
        BatchCompressor.__init__( self
                                , additional_compressors = settings.COMPRESS_CSS_COMPRESSORS
                                , verbose = verbose )

    def concatenate(self, paths):
        """Concatenate together files and rewrite urls"""
        stylesheets = []
        for path in paths:
            def reconstruct(match):
                asset_path = match.group(1)
                if asset_path.startswith("http://") \
                       or asset_path.startswith("https://") \
                       or os.path.isabs(asset_path):
                    return "url(%s)" % asset_path
                asset_url = urlparse.urljoin(
                    settings.COMPRESS_URL,
                    self.construct_asset_path(asset_path, path)
                )
                return "url(%s)" % asset_url
            content = self.read_file(path)
            content = re.sub(URL_DETECTOR, reconstruct, content)
            stylesheets.append(content)
        return '\n'.join(stylesheets)

    def construct_asset_path(self, asset_path, css_path):
        if os.path.isabs(asset_path):
            return asset_path
        public_path = self.absolute_path(asset_path, css_path)
        return make_relative_path(public_path)

    def absolute_path(self, asset_path, css_path):
        if os.path.isabs(asset_path):
            path = os.path.join(settings.COMPRESS_ROOT, asset_path)
        else:
            path = os.path.join(os.path.dirname(css_path), asset_path)
        return os.path.normpath(path)

class CompressorError(Exception):
    """This exception is raised when a filter fails"""
    pass

class SubProcessCompressor(BaseCompressor):
    def execute_command(self, command, content):
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        if content:
            pipe.stdin.write(content)
        pipe.stdin.close()

        compressed_content = pipe.stdout.read()
        pipe.stdout.close()

        error = pipe.stderr.read()
        pipe.stderr.close()

        if pipe.wait() != 0:
            if not error:
                error = "Unable to apply %s compressor" % self.__class__.__name__
            raise CompressorError(error)

        if self.verbose:
            print error

        return compressed_content

