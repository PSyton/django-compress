.. _ref-backwardsincompatiblechanges:

==============================
Backwards Incompatible Changes
==============================

A list of backwards incompatible changes

Version 1.2
===========

* CSSTidy isn't the default anymore, YUI Compressor is now the default.
* Filters are now called compressors.

Revision 53
===========

http://code.google.com/p/django-compress/source/detail?r=53

Changed the default media type for CSS to "all" instead of "media,projection".

You can still specify media type with `extra_context`.

Revision 56
===========

http://code.google.com/p/django-compress/source/detail?r=56

*bump_filename completely changed*

bump_filename was broken because a lot of caches does not properly cache files with querystrings.
Therefore it is completely rewritten without any thoughts on backwards compatibility, since it was not possible anyways.
This changeset also introduces a couple of other changes that could potentially break old code.

* The `bump_filename` option was removed from the group settings. There is no need specifying it for ALL groups, if you actually use it, you most likely want to use it on all your compressed files.
* The bump_filename options is replaced by the setting COMPRESS_VERSION, and is completely ignored.
* The querystring is no longer used to determine a files version, since it was use
* If ``COMPRESS_VERSION`` is used, you specify the version part of the `output_filename` file with '?'. This placeholder can be changed with COMPRESS_VERSION_PLACEHOLDER. 

E.g.::
  
  'screen': {
      'source_filenames': ('css/screen/style.css', 'css/screen/paginator.css', 'css/screen/agenda.css', 'css/screen/weather.css', 'css/screen/gallery.css', ),
      'output_filename': 'c/screen.r?.css',
  },

* ``COMPRESS_VERSION`` requires ``COMPRESS_AUTO`` to be enabled.
  ``COMPRESS_AUTO`` is enabled by default, but if you explicitly set it to ``False`` an ``ImproperlyConfiguredError`` exception will be thrown. 

``COMPRESS_AUTO`` changes

* The CSS/Javascript files are not checked during Django's initialization anymore.
  It was not really useful and did not make sense.
  The automatic part is now handled by the templatetags (i.e. what used to be ``COMPRESS_TEMPLATE_AUTO``).
* ``COMPRESS_AUTO`` is replaced by ``COMPRESS_AUTO_TEMPLATE``, and the old behavior
  of ``COMPRESS_AUTO`` is removed. This might be really confusing, the :doc:`configuration` should make it clear. 