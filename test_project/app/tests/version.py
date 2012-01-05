from django.test import TestCase
from compress.conf import settings
from compress.versioning import Versioning
import os

js_list = ['js/application1.js', 'js/application2.js', 'js/non_existance.js']


class VersioningTest(TestCase):
    root_path = os.path.join(os.path.dirname(__file__), "testdata/")

    def test_time_versioning(self):
        settings.COMPRESS_VERSIONING = "compress.versioning.mtime.MTimeVersioning"

        v = Versioning()
        self.assertTrue(v.version(js_list)>0)

    def test_cleanup(self):
	# todo write for all versions...
        settings.COMPRESS_VERSIONING = "compress.versioning.mtime.MTimeVersioning"

	# Create temporary file then try to call cleanup for it.
        v = Versioning()
        filename = 'file.r?.xxx'
        fn = v.output_filename(filename, js_list)
        
        f = open(os.path.join(settings.COMPRESS_ROOT, fn), 'rw+')
        f.close()
        v.cleanup(filename)

	# todo check that file doesn't exist...

