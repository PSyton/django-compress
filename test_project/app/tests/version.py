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
        fn = v.output_filename(filename, None)

        f = open(fn, 'w+')
        f.close()

        version = v.version_from_file(os.path.dirname(fn), filename)
        self.assertTrue(version == '0')

        v.cleanup(filename)
        self.assertFalse(os.path.exists(fn))

        # todo check that file doesn't exist...

