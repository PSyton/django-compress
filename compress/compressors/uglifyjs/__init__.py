from compress.conf import settings
from compress.compressors import SubProcessCompressor


class UglifyJSCompressor(SubProcessCompressor):

    def executable(self):
        return settings.COMPRESS_UGLIFYJS_BINARY

    def options(self):
        opts = '-nc %s' % settings.COMPRESS_UGLIFYJS_ARGUMENTS
        if self.verbose:
            opts += ' --verbose'
        return opts
