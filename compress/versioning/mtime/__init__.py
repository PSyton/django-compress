import time
from compress.storage import storage
from compress.versioning import VersioningBase


class MTimeVersioning(VersioningBase):
    def version(self, paths):
        # Return the modification time for the newest source file
        return str(max([self.time_for_file(path) for path in paths]))

    def time_for_file(self, path):
        return int(time.mktime(storage.modified_time(path).timetuple()))

    def need_update(self, output_file, paths, version):
        output_filename = self.output_filename(output_file, version)
        return (self.time_for_file(output_filename) < int(version)), version
