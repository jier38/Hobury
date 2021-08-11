# -*- coding: utf-8 -*-
"""
Trac plugin proving a full-featured, self-contained Blog.

License: BSD

(c) 2007 ::: www.CodeResort.com - BV Network AS (simon-code@bvnetwork.no)
"""

from setuptools import setup

setup(name='Trade',
      version='2.0',
      packages=['trade'],
      author='Hobury Investments',
      author_email='',
      keywords='trac trade',
      description='',
      url='',
      license='BSD',
      zip_safe=False,
      extras_require={},
      entry_points={'trac.plugins': [
          'trade.web_ui = trade.web_ui']},
      package_data={'trade': ['htdocs/*.png',
                              'htdocs/css/*.css',
                              'htdocs/js/*.js',
                              'templates/*.html',
                              'templates/*.rss', ]},
      exclude_package_data={},
      test_suite='',
      tests_require=[],
      install_requires=[])
