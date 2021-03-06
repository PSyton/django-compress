import glob
import os
import urlparse

from compress.conf import settings
from compress.compilers import Compiler
from compress.compressors import JSCompressor, CSSCompressor
from compress.signals import css_compressed, js_compressed
from compress.storage import storage
from compress.versioning import Versioning
from compress.utils import make_relative_path, makeDirs


class Packager(object):
    def __init__(self, force=False, verbose=False):
        self.force = force
        self.verbose = verbose
        self.versioning = Versioning(verbose)
        self.compiler = Compiler(verbose)
        self.packages = {
            'css': self.create_packages(settings.COMPRESS_CSS),
            'js': self.create_packages(settings.COMPRESS_JS),
        }
        for kind in ['css', 'js']:
            for p in self.packages[kind]:
                self.packages[kind][p]['type'] = kind

    def package_for(self, kind, package_name):
        try:
            return self.packages[kind][package_name].copy()
        except KeyError:
            raise PackageNotFound(
                "No corresponding package for %s package name : %s" % (
                    kind, package_name
            )
        )

    def individual_url(self, filename):
        return urlparse.urljoin(settings.COMPRESS_URL,
            make_relative_path(filename))

    def compile(self, paths):
        return self.compiler.compile(paths)

    def pack(self, package):
        if 'output' not in package \
            or 'type' not in package \
            or not package['output'] \
            or not package['type'] \
            or len(package['paths']) == 0:
            return ''
        if package['type'] == 'css':
              compressor = CSSCompressor(self.verbose)
              signal = css_compressed
        else:
              compressor = JSCompressor(self.verbose)
              signal = js_compressed
        if settings.COMPRESS_AUTO or self.force:
            need_update, version = self.versioning.need_update(
                package['output'], package['paths'])
            if need_update or self.force:
                output_filename = self.versioning.output_filename(
                    package['output'],
                    self.versioning.version(package['paths']))
                self.versioning.cleanup(package['output'])
                if self.verbose or self.force:
                    print "Version: %s" % version
                    print "Saving: %s" % make_relative_path(output_filename)
                paths = self.compile(package['paths'])
                content = compressor.compress(paths)
                if not self.save_file(output_filename, content):
                    return ''
                signal.send(sender=self, package=package, version=version)
        else:
            filename_base, filename = os.path.split(package['output'])
            version = self.versioning.version_from_file(filename_base,
                                                        filename)
        return self.versioning.output_filename(package['output'], version)

    def save_file(self, filename, content):
        try:
            makeDirs(filename)
            file = storage.open(filename, mode='wb+')
            file.write(content.encode('utf8'))
            file.close()
        except Exception:
            return False
        return True

    def create_packages(self, config):
        packages = {}
        if not config:
            return packages
        packages = {}
        for name in config:
            packages[name] = {}
            paths = []
            if 'source_filenames' in config[name]:
                for path in config[name]['source_filenames']:
                    full_path = os.path.normpath(
                        os.path.join(settings.COMPRESS_ROOT, path))
                    norm_root = os.path.normpath(settings.COMPRESS_ROOT) + '/'
                    for path in glob.glob(full_path):
                        path = os.path.normpath(path).replace(norm_root, '')
                        if not path in paths:
                            paths.append(path)
            packages[name]['paths'] = paths
            if 'output_filename' in config[name]:
                packages[name]['output'] = config[name]['output_filename']
            else:
                packages[name]['output'] = ''
            packages[name]['context'] = {}
            if 'extra_context' in config[name]:
                packages[name]['context'] = config[name]['extra_context']
            if 'template_name' in config[name]:
                packages[name]['template'] = config[name]['template_name']
            if 'external_urls' in config[name]:
                packages[name]['externals'] = config[name]['external_urls']
        return packages


class PackageNotFound(Exception):
    pass
