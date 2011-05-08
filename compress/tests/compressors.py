from django.test import TestCase
from compress.conf import settings
from compress.compressors import CSSCompressor, JSCompressor, SubProcessCompressor
import os

class CompressorTest(TestCase):
    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        settings.COMPRESS_URL = 'http://localhost/static/'
        self.old_root = settings.COMPRESS_ROOT
        settings.COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "testdata/")

    def test_css_concatenate(self):
        compressor = CSSCompressor()
        css_list = [ 'absolute.css'
               , 'relative.css'
               , 'no_protocol.css'
               , 'utf8.css' ]
        output = compressor.compress( css_list )
        f = open( os.path.join( settings.COMPRESS_ROOT, 'results1.css' ), 'rb' )
        self.assertEqual( f.read().decode('utf8'), output, "CSS concatenate failed")
        f.close()

    def test_js_concatenate(self):
        compressor = JSCompressor()
        js_list = [ 'application1.js'
                  , 'application2.js' ]
        output = compressor.compress( js_list )
        f = open( os.path.join( settings.COMPRESS_ROOT, 'results1.js' ), 'rb' )
        self.assertEqual( f.read().decode('utf8'), output, "JS concatenate failed")
        f.close()

    def test_subprocess_compressor(self):
        compresstor = SubProcessCompressor( False )
        f = open( os.path.join( settings.COMPRESS_ROOT, 'results1.js' ), 'rb' )
        data = f.read()
        f.close()
        out = compresstor.execute_command( "cat", data )
        self.assertEqual( out, data, 'Wrong command output expected "%s", got "%s"' % ( data, out ) )

    def tearDown(self):
        settings.COMPRESS_URL = self.old_compress_url
        settings.COMPRESS_ROOT = self.old_root


