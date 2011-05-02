from django.test import TestCase
from compress.conf import settings

class CompressorTest(TestCase):
    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        settings.COMPRESS_URL = 'http://localhost/static/'

    def test_url_rewrite(self):
        compressor = Compressor()
        output = compressor.concatenate_and_rewrite([
            os.path.join(settings.COMPRESS_ROOT, 'css/urls.css'),
        ])
        self.assertEquals(""".relative-url {
  background-image: url(http://localhost/static/images/sprite-buttons.png);
}
.absolute-url {
  background-image: url(http://localhost/images/sprite-buttons.png);
}
.no-protocol-url {
  background-image: url(//images/sprite-buttons.png);
}""", output)

    def tearDown(self):
        settings.COMPRESS_URL = self.old_compress_url


