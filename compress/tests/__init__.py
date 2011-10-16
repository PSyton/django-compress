import compress
from compress.tests.compilers import *
from compress.tests.compressors import *
from compress.tests.config import *
from compress.tests.package import *
from compress.tests.templatetags import *

class CompressVersionInfoTests(TestCase):
    """
    Test django-compress's internal version-reporting
    infrastructure.

    """
    def setUp(self):
        self.version = compress.VERSION

    def tearDown(self):
        compress.VERSION = self.version

    def test_get_version(self):
        """
        Test the version-info reporting.

        """
        versions = [
            {'version': (1, 0, 0, 'alpha', 0),
             'expected': "1.0 pre-alpha"},
            {'version': (1, 0, 1, 'alpha', 1),
             'expected': "1.0.1 alpha 1"},
            {'version': (1, 1, 0, 'beta', 2),
             'expected': "1.1 beta 2"},
            {'version': (1, 2, 1, 'rc', 3),
             'expected': "1.2.1 rc 3"},
            {'version': (1, 3, 0, 'final', 0),
             'expected': "1.3"},
            {'version': (1, 4, 1, 'beta', 0),
             'expected': "1.4.1 beta"},
            ]

        for version_dict in versions:
            compress.VERSION = version_dict['version']
            self.assertEqual(compress.get_version(), version_dict['expected'])

