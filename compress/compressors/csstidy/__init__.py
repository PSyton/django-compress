import os
import warnings
import tempfile

from compress.conf import settings
from compress.compressors import BaseCompressor

warnings.simplefilter('ignore', RuntimeWarning)


class CSSTidyCompressor(BaseCompressor):
    def compress(self, css):
        tmp_file = tempfile.NamedTemporaryFile(mode='w+b')
        tmp_file.write(css)
        tmp_file.flush()

        output_file = tempfile.NamedTemporaryFile(mode='w+b')

        command = '%s %s %s %s' % (
            settings.COMPRESS_CSSTIDY_BINARY, tmp_file.name,
            settings.COMPRESS_CSSTIDY_ARGUMENTS, output_file.name
        )

        command_output = os.popen(command).read()

        filtered_css = output_file.read()
        output_file.close()
        tmp_file.close()

        if self.verbose:
            print command_output

        return filtered_css
