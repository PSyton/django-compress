.. _ref-installation:

============
Installation
============

Installation is pretty straight-forward and follows the same installation
procedure as many other *Django* applications.

``django-compress`` does not create any models, so you do not need to configure a database.

Install instructions
====================

1. Either check out django-compress from GitHub_ or to pull a release off PyPI_.
   Doing ``pip install django-compress`` or ``easy_install django-compress`` is all that should be required.

2. Add 'compress' to your ``INSTALLED_APPS``


.. _GitHub: http://github.com/pelme/django-compress
.. _PyPI: http://pypi.python.org/

Recommendations
===============

By default django-compress uses YUI Compressor to compress CSS and JS.
YUI Compressor is an excellent stand-alone application for dealing with JS and CSS-files.

If you do not install YUI COMPRESSOR, make sure to disable the compressor in your settings.

YUI Compressor can be downloaded from: http://developer.yahoo.com/yui/compressor/.
Alternatively your distros package manager may be able to install it for you.

If you download YUI Compressor from the yahoo site you will need to build it. You will need to install ``ant`` - an example install (using the ``yum`` package manager to install ``ant``) is shown ::

    $ wget http://yui.zenfs.com/releases/yuicompressor/yuicompressor-2.4.6.zip
    $ unzip yuicompressor-2.4.6.zip
    $ cd yuicompressor-2.4.6/
    $ yum install ant
    $ ant build

You will then need to point django-compress at the installed jar file - see the :doc:`installation` section for more details.
