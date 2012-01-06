import os
import re

from compress.conf import settings
from compress.storage import storage
from compress.utils import to_class, root_path


class Versioning(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def versionner(self):
        return to_class(settings.COMPRESS_VERSIONING)(self)
    versionner = property(versionner)

    def version(self, paths):
        return getattr(self.versionner, 'version')(paths)

    def placeholder(self):
        return settings.COMPRESS_VERSION_PLACEHOLDER

    def file_regex(self, filename):
        filename = r'([A-Za-z0-9]+)'.join(
                            [re.escape(part) \
                             for part in filename.split(self.placeholder())])
        return re.compile(r'^%s$' % filename)

    def version_from_file(self, path, filename):
        regex = self.file_regex(filename)
        versions = []
        for f in sorted(storage.listdir(path)[1], reverse=True):
            version = regex.match(f)
            if version and version.groups():
                versions.append(version.group(1))
        versions.sort()
        return versions[-1]

    def output_filename(self, filename, version):
        if settings.COMPRESS_VERSION and version is not None:
            output_filename = filename.replace(self.placeholder(),
                version)
        else:
            output_filename = filename.replace(self.placeholder(),
                settings.COMPRESS_VERSION_DEFAULT)
        output_path = root_path(output_filename)
        return os.path.normpath(output_path)

    def need_update(self, output_file, paths):
        version = self.version(paths)
        output_file = self.output_filename(output_file, version)
        if not storage.exists(root_path(output_file)):
            return True, version
        return getattr(self.versionner, 'need_update')(output_file, paths, version)

    def cleanup(self, filename):
        if not settings.COMPRESS_VERSION \
            and not settings.COMPRESS_VERSION_REMOVE_OLD:
            return  # Nothing to delete here
        path = os.path.dirname(filename)
        regex = self.file_regex(os.path.basename(filename))
        if storage.exists(path):
            for f in storage.listdir(path)[1]:
                if regex.match(f):
                    if self.verbose:
                        print "Removing outdated file %s" % f
                    storage.delete(os.path.join(path, f))


class VersioningBase(object):
    def __init__(self, versioning):
        self.versioning = versioning

    def output_filename(self, filename, version):
        return self.versioning.output_filename(filename, version)

    def version(self, source_files):
        raise NotImplementedError

    def needs_update(self, output_file, paths, version):
        raise NotImplementedError


class VersioningError(Exception):
    """This exception is raised when version creation fails"""
    pass
