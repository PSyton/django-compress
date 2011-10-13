from compress.compressors import BaseCompressor
from compress.compressors.jsmin.jsmin import jsmin


class JSMinCompressor(BaseCompressor):
    def compress(self, js):
        return jsmin(js)

    def available(self):
        return True
