import tempfile

from compress.conf import settings
from compress.compressors import SubProcessCompressor

class CSSTidyCompressor(SubProcessCompressor):

    def executable(self):
        return settings.COMPRESS_CSSTIDY_BINARY

    def compress(self, css):
        tmp_file = tempfile.NamedTemporaryFile(mode='w+b')
        tmp_file.write( css.encode( 'utf8' ) )
        tmp_file.flush()

        output_file = tempfile.NamedTemporaryFile(mode='w+b')

        command = '%s %s %s %s' % (
            executable(self), tmp_file.name,
            settings.COMPRESS_CSSTIDY_ARGUMENTS, output_file.name
        )

        command_output = self.execute_command( command, None )

        output_file.seek( 0 )
        filtered_css = output_file.read()
        output_file.close()
        tmp_file.close()

        if self.verbose:
            print command_output

        return filtered_css
