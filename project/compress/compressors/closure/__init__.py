from compress.conf import settings
from compress.compressors import SubProcessCompressor


class ClosureCompressor(SubProcessCompressor):
    def executable(self):
        return settings.COMPRESS_CLOSURE_BINARY

    def options(self):
        opts = settings.COMPRESS_CLOSURE_ARGUMENTS
        if self.verbose:
            opts += ' --verbose'
        return opts
