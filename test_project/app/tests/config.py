from django.test import TestCase
from compress.conf import settings


class TrailingslashesTest(TestCase):
    def test_slashes(self):
        self.assertTrue( settings.COMPRESS_ROOT[-1] == '/' )
        self.assertTrue( settings.COMPRESS_URL[-1] == '/' )

