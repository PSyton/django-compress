.. _ref-features:

========
Features
========

This is a application that will provide an easy and automated way to output
compressed/minified CSS and JavaScript.
It adheres to the DRY principle, you set up your CSS-files and JavaScript-files
in your project settings, and you are done.
There is no need to enter the names in your template again (a couple of template tags takes care of that).

* Group and concatenate your stylesheets and jaavscripts source files to single files,
  and run the code through specified compressors.

* Provides sane defaults for CSS and JavaScript minification (YUI compressor required).

* A compressor for **YUI Compressor**, **Google Closure Compiler**, **UglifyJS** is included.

* It’s easy and straightforward to write custom compressors to generate the output.

* A last-modification and/or version part can automatically be appended to the filename
  of the outputted files to make use of “far future Expires HTTP header),
  and provide an automated way of updating the content without delays.

* You setup and group your CSS and JavaScript-files in the settings,
  and set up whetter or not you want your files to be compressed.

* Templatetags to output CSS (``<link>``) or JavaScript (``<script>``) tags
  with the compressed files if ``COMPRESS = True``, or otherwise the source files.

* The compressed files will be updated (if needed) when you are accessing them
  from the templatetags.
  
  This only applies when ``COMPRESS_AUTO`` is enabled.
  You can manually update them with ``./manage.py synccompress``.
