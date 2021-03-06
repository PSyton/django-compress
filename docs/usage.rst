.. _ref-usage:

=====
Usage
=====

Describes how to use django-compress when it is installed and configured.

Automated generation
====================

If ``COMPRESS`` and ``COMPRESS_AUTO`` is enabled (``True``), the source files
will be automatically updated, and re-generated if needed when invoked from the
templatetags.
The last modified time of the files will be compared, and if any of the
source-files is newer than the output-file, the file will be re-generated.

Management command
==================

You can update and force updates of the compressed file(s) with the management command “synccompress”.
This makes it possible to keep the files updated manually.

The command is (assuming you are in you project-folder that contains ``manage.py``). ::

    ./manage.py synccompress

To force all files to be re-generated, use the argument ``--force`` :: 
  
    ./manage.py synccompress --force

Templatetags
============

django-compress includes two template tags: ``compressed_css`` and ``compressed_js``,
in a template library called ``compressed``.

They are used to output the ``<link>`` and ``<script>``-tags for the
specified CSS/JavaScript-groups (as specified in the settings).
The first argument must be the name of the CSS/JavaScript group.

The templatetags will either output the source filenames or the compressed filenames,
depending on the ``COMPRESS`` setting, if you do not specify the ``COMPRESS`` setting,
the source files will be used in DEBUG-mode, and compressed files in non-DEBUG-mode.

Example
-------

If you have specified the CSS-groups “screen” and “print” and a JavaScript-group
with the name “scripts”, you would use the following code to output them all ::

   {% load compressed %}
   {% compressed_css 'screen' %}
   {% compressed_css 'print' %}
   {% compressed_js 'scripts' %}
