from django.test import TestCase
from compress.conf import settings
from compress.compressors import CSSCompressor, JSCompressor
from compress.compressors import SubProcessCompressor, BaseCompressor
import os
import glob


class BadCompressor(BaseCompressor):

    def compress(self, content):
        pass


css_list = ['css/absolute.css', 'css/relative.css',
            'css/no_protocol.css', 'css/utf8.css']

js_list = ['js/application1.js', 'js/application2.js']


class CompressorTest(TestCase):
    root_path = os.path.join(os.path.dirname(__file__), "testdata/")

    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        self.old_root = settings.COMPRESS_ROOT
        self.old_css_compressors = settings.COMPRESS_CSS_COMPRESSORS
        self.old_js_compressors = settings.COMPRESS_JS_COMPRESSORS
        settings.COMPRESS_ROOT = os.path.join(os.path.dirname(__file__),
                                              "testdata/")
        settings.COMPRESS_URL = 'http://localhost/static/'
        settings.COMPRESS_CSS_COMPRESSORS = []
        settings.COMPRESS_JS_COMPRESSORS = []

    def test_css_concatenate(self):
        settings.COMPRESS_CSS_COMPRESSORS = []
        settings.COMPRESS_ROOT = os.path.join(os.path.dirname(__file__),
                                              "testdata/")
        compressor = CSSCompressor()
        output = compressor.compress(css_list)
        test_file = open(os.path.join(settings.COMPRESS_ROOT,
                              'css/results1.css'), 'rb')
        self.assertEqual(test_file.read().decode('utf8'), output)
        test_file.close()

    def test_js_concatenate(self):
        settings.COMPRESS_JS_COMPRESSORS = []
        compressor = JSCompressor()
        output = compressor.compress(js_list)
        test_file = open(os.path.join(settings.COMPRESS_ROOT,
                              'js/results1.js'), 'rb')
        self.assertEqual(test_file.read().decode('utf8'), output)
        test_file.close()

    def test_subprocess_compressor(self):
        compressor = SubProcessCompressor(False)
        test_file = open(os.path.join(settings.COMPRESS_ROOT,
                                      'js/results1.js'), 'rb')
        data = test_file.read()
        test_file.close()
        out = compressor.execute_command("cat", data)
        self.assertEqual(out, data,
                'Wrong command output expected "%s", got "%s"' % (data, out))

    def test_basecompressor(self):
        with self.assertRaises(NotImplementedError):
            BaseCompressor(False).compress("test content")

    def test_csstidy(self):
        tidy = glob.glob(settings.COMPRESS_CSSTIDY_BINARY)
        if tidy:
            settings.COMPRESS_CSS_COMPRESSORS = [
              'compress.compressors.csstidy.CSSTidyCompressor']
            compressor = CSSCompressor()
            output = compressor.compress(css_list)
            test_file = open(os.path.join(settings.COMPRESS_ROOT,
                                   'css/results_tidy.css'), 'rb')
            self.assertEqual(test_file.read().decode('utf8'), output)
            test_file.close()

    def test_jsmin(self):
        settings.COMPRESS_JS_COMPRESSORS = [
          'compress.compressors.jsmin.JSMinCompressor']
        compressor = JSCompressor()
        output = compressor.compress(js_list)
        test_file = open(os.path.join(settings.COMPRESS_ROOT,
                               'js/results_jsmin.js'), 'rb')
        self.assertEqual(test_file.read().decode('utf8'), output)
        test_file.close()

    def tearDown(self):
        settings.COMPRESS_URL = self.old_compress_url
        settings.COMPRESS_ROOT = self.old_root
        settings.COMPRESS_CSS_COMPRESSORS = self.old_css_compressors
        settings.COMPRESS_JS_COMPRESSORS = self.old_js_compressors
