# -*- coding: utf-8 -*-
"""
Trac plugin proving a full-featured, self-contained Blog.

License: BSD

(c) 2007 ::: www.CodeResort.com - BV Network AS (simon-code@bvnetwork.no)
"""

from setuptools import setup

setup(name='Download',
      version='2.0',
      packages=['download'],
      author='Hobury Investments',
      author_email='',
      keywords='trac download',
      description='',
      url='',
      license='BSD',
      zip_safe=False,
      extras_require={},
      entry_points={'trac.plugins': [
          'download.web_ui = download.web_ui']},
      package_data={'download': ['htdocs/*.png',
                                 'htdocs/css/*.css',
                                 'htdocs/js/*.js',
                                 'templates/*.html',
                                 'templates/*.rss', ]},
      exclude_package_data={},
      test_suite='',
      tests_require=[],
      install_requires=[])
