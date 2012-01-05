from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from compress.conf import settings as compress_settings
import os

COMPRESS_CSS = {
  'test_css': {
    'source_filenames': (
       'css/absolute.css',
       'css/relative.css',
       'css/no_protocol.css',
       'css/utf8.css'
       ),
    'output_filename': 'css/compressed/common.css',
    'extra_context': {
            'media': 'screen,projection',
    },
  },
}

COMPRESS_JS = {
  'test_js': {
    'external_urls': (
        'http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js'
      , 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.7/jquery-ui.min.js'
    , ),
    'source_filenames': (
        'js/application1.js',
        'js/application2.js',
        'js/application4.js'
    ),
    'output_filename': 'js/compressed/all.js',
  },
}

class TemplateTagsTest(TestCase):
  urls = 'app.tests.urls'

  def setUp(self):
    self.old_template_dirs = getattr(settings, 'TEMPLATE_DIRS')
    settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
    self.old_compress_url = compress_settings.COMPRESS_URL
    self.old_root = compress_settings.COMPRESS_ROOT
    self.old_css = compress_settings.COMPRESS_CSS
    self.old_js = compress_settings.COMPRESS_JS
    self.old_compress = compress_settings.COMPRESS
    compress_settings.COMPRESS = True
    compress_settings.COMPRESS_URL = 'http://localhost/static/'
    compress_settings.COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "testdata/")
    compress_settings.COMPRESS_CSS = COMPRESS_CSS
    compress_settings.COMPRESS_JS = COMPRESS_JS

  def tearDown(self):
    compress_settings.COMPRESS = self.old_compress
    settings.TEMPLATE_DIRS = self.old_template_dirs
    compress_settings.COMPRESS_URL = self.old_compress_url
    compress_settings.COMPRESS_ROOT = self.old_root
    compress_settings.COMPRESS_CSS = self.old_css
    compress_settings.COMPRESS_JS = self.old_js

  def test_tags_work(self):
    response = self.client.get(reverse('test-compress-templatetags'))
    self.assertEqual(response.status_code, 200)
    self.assertTrue( response.content.count( '<link href="http://localhost/static/css/compressed/common.css" rel="stylesheet" type="text/css" media="screen,projection" />' ) == 1 )
