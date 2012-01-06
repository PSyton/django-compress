import cStringIO
from hashlib import md5, sha1
from compress.storage import storage
from compress.versioning import VersioningBase


class HashVersioningBase(VersioningBase):
    def __init__(self, versioning, hash_method):
        super(HashVersioningBase, self).__init__(versioning)
        self.hash_method = hash_method

    def need_update(self, output_file, paths, version):
        output_file_name = self.output_filename(output_file, version)
        try:
            start = output_file.index(self.placeholder())
            stop = start + len(self.placeholder()) - len(output_file)
            old_version = output_file_name[start:stop]
            return (version != old_version), version
        except ValueError:
            # no placeholder found, do not update, manual update if needed
            return False, version

    def concatenate(self, paths):
        """Concatenate together a list of files"""
        return '\n'.join([self.read_file(path) for path in paths])

    def read_file(self, path):
        """Read file content in binary mode"""
        file = storage.open(path, 'rb')
        content = file.read()
        file.close()
        return content

    def version(self, paths):
        buf = self.concatenate(paths)
        s = cStringIO.StringIO(buf)
        version = self.get_hash(s)
        s.close()
        return version

    def get_hash(self, f, CHUNK=2 ** 16):
        m = self.hash_method()
        while 1:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            m.update(chunk)
        return m.hexdigest()


class MD5Versioning(HashVersioningBase):
    def __init__(self, versioning):
        super(MD5Versioning, self).__init__(versioning, md5)


class SHA1Versioning(HashVersioningBase):
    def __init__(self, versioning):
        super(SHA1Versioning, self).__init__(versioning, sha1)
