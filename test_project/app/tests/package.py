import os
from django.test import TestCase
from compress.conf import settings
from compress.packager import Packager, PackageNotFound


class PackagerTest(TestCase):

    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        settings.COMPRESS_URL = 'http://localhost/static/'
        self.maxDiff = None

    def test_individual_url(self):
        """Check that individual URL is correctly generated"""
        packager = Packager()
        filename = os.path.join(settings.COMPRESS_ROOT, u'js/application.js')
        individual_url = packager.individual_url(filename)
        self.assertEqual(individual_url,
                         settings.COMPRESS_URL + "js/application.js")

    def test_create_package(self):
        packager = Packager()
        self.assertEqual(packager.create_packages( {} ), {})

        with self.assertRaises( PackageNotFound ):
          packager.package_for('css', 'test_package')

        old_root = settings.COMPRESS_ROOT
        settings.COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "testdata/")
        packages = { 'data': { 'jquery': { 'external_urls': ('http://ajax.googleapis.com/ajax/libs/jquery/1.6.0/jquery.min.js',) }
                             , 'main': { 'source_filenames': ( 'js/application.js'
                                                             , 'js/application1.js'
                                                             , )
                                       , 'output_filename': 'application.r?.js' }
                             , 'mixed': { 'external_urls': ('http://ajax.googleapis.com/ajax/libs/jquery/1.6.0/jquery.min.js',)
                                        , 'source_filenames': ('js/application.js'
                                                             , 'js/application1.js'
                                                             , )
                                        , 'output_filename': 'application.r?.js' }
                             , 'test': { 'source_filenames': ( 'css/abs*.css'
                                                             , )
                                       , 'output_filename': 'application.r?.css'
                                       , 'template_name': 'test/template.html'
                                       , 'extra_context': { 'a': 'a', } }
                             }
                   , 'expected': { 'jquery': { 'context': {}
                                             , 'externals': ('http://ajax.googleapis.com/ajax/libs/jquery/1.6.0/jquery.min.js',)
                                             , 'output': ''
                                             , 'paths': [] }
                                 , 'main': { 'context': {}
                                           , 'output': 'application.r?.js'
                                           , 'paths': ['js/application1.js'] }
                                 , 'mixed': { 'context': {}
                                            , 'externals': ('http://ajax.googleapis.com/ajax/libs/jquery/1.6.0/jquery.min.js',)
                                            , 'output': 'application.r?.js'
                                            , 'paths': ['js/application1.js'] }
                                 , 'test': { 'context': { 'a': 'a' }
                                           , 'paths': [ 'css/absolute.css' ]
                                           , 'output': 'application.r?.css'
                                           , 'template': 'test/template.html' }
                                 }
                   }
        out = packager.create_packages( packages['data'] )
        self.assertEqual(out, packages['expected'] )
        settings.COMPRESS_ROOT = old_root

    def tearDown(self):
        settings.COMPRESS_URL = self.old_compress_url

