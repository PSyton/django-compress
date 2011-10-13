from django.utils import importlib
import os
from conf import settings

def to_class(class_str):
    module_bits = class_str.split('.')
    module_path, class_name = '.'.join(module_bits[:-1]), module_bits[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_name, None)

def make_relative_path(absolute_path):
    out = absolute_path
    if absolute_path[0] == '/':
      compress_root = os.path.normpath(settings.COMPRESS_ROOT) + "/"
      out = os.path.normpath( absolute_path ).replace(compress_root, '')
    return out

def root_path(filename):
    return os.path.join(settings.COMPRESS_ROOT, filename)

def makeDirs(filename):
  dir = os.path.dirname(filename)
  if not os.path.exists(dir):
    os.makedirs(dir)
