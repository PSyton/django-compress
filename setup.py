from setuptools import setup, find_packages
from compress import get_version
setup(
    name='django-compress',
    version=get_version(),
    description='django-compress provides an automated system for compressing CSS and JavaScript files',
    author='Andreas Pelme',
    author_email='Andreas Pelme <andreas@pelme.se>',
    url='http://code.google.com/p/django-compress/',
    packages=find_packages(exclude=['test_project']),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
