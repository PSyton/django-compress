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
        print v.version(js_list)
