from django.test import TestCase
from compress.conf import settings
from compress.compressors import CSSCompressor, JSCompressor, SubProcessCompressor, BaseCompressor
import os, glob

class BadCompressor(BaseCompressor):
  pass

css_list = [ 'css/absolute.css'
           , 'css/relative.css'
           , 'css/no_protocol.css'
           , 'css/utf8.css' ]

js_list = [ 'js/application1.js'
          , 'js/application2.js' ]

class CompressorTest(TestCase):
    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        self.old_root = settings.COMPRESS_ROOT
        self.old_css_compressors = settings.COMPRESS_CSS_COMPRESSORS
        self.old_js_compressors = settings.COMPRESS_JS_COMPRESSORS
        settings.COMPRESS_URL = 'http://localhost/static/'
        settings.COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "testdata/")
        settings.COMPRESS_CSS_COMPRESSORS = []
        settings.COMPRESS_JS_COMPRESSORS = []

    def test_css_concatenate(self):
        settings.COMPRESS_CSS_COMPRESSORS = []
        compressor = CSSCompressor()
        output = compressor.compress( css_list )
        f = open( os.path.join( settings.COMPRESS_ROOT, 'css/results1.css' ), 'rb' )
        self.assertEqual( f.read().decode('utf8'), output)
        f.close()

    def test_js_concatenate(self):
        settings.COMPRESS_JS_COMPRESSORS = []
        compressor = JSCompressor()
        output = compressor.compress( js_list )
        f = open( os.path.join( settings.COMPRESS_ROOT, 'js/results1.js' ), 'rb' )
        self.assertEqual( f.read().decode('utf8'), output)
        f.close()

    def test_subprocess_compressor(self):
        compresstor = SubProcessCompressor( False )
        f = open( os.path.join( settings.COMPRESS_ROOT, 'js/results1.js' ), 'rb' )
        data = f.read()
        f.close()
        out = compresstor.execute_command( "cat", data )
        self.assertEqual( out, data, 'Wrong command output expected "%s", got "%s"' % ( data, out ) )

    def test_basecompressor(self):
        with self.assertRaises(NotImplementedError):
            BaseCompressor( False ).compress("test content")

    def test_csstidy(self):
      tidy = glob.glob( settings.COMPRESS_CSSTIDY_BINARY )
      if tidy:
        settings.COMPRESS_CSS_COMPRESSORS = [ 'compress.compressors.csstidy.CSSTidyCompressor' ]
        compressor = CSSCompressor()
        output = compressor.compress( css_list )
        f = open( os.path.join( settings.COMPRESS_ROOT, 'css/results_tidy.css' ), 'rb' )
        self.assertEqual( f.read().decode('utf8'), output)
        f.close()

    def test_jsmin(self):
      settings.COMPRESS_JS_COMPRESSORS = [ 'compress.compressors.jsmin.JSMinCompressor' ]
      compressor = JSCompressor()
      output = compressor.compress( js_list )
      f = open( os.path.join( settings.COMPRESS_ROOT, 'js/results_jsmin.js' ), 'rb' )
      self.assertEqual( f.read().decode('utf8'), output)
      f.close()


    def tearDown(self):
        settings.COMPRESS_URL = self.old_compress_url
        settings.COMPRESS_ROOT = self.old_root
        settings.COMPRESS_CSS_COMPRESSORS = self.old_css_compressors
        settings.COMPRESS_JS_COMPRESSORS = self.old_js_compressors


