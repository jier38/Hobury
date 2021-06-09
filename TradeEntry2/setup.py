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
      author='John Huang',
      author_email='jier38@gmail.com',
      keywords='trac trade',
      description='',
      url='',
      license='BSD',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Plugins',
                   'Environment :: Web Environment',
                   'Framework :: Trac',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3.7',
                   ],
      zip_safe = False,
      extras_require={},
      entry_points={'trac.plugins': [
            'trade.web_ui = trade.web_ui']},
      package_data={'trade' : ['htdocs/*.png',
                                      'htdocs/css/*.css',
                                      'htdocs/js/*.js',
                                      'templates/*.html',
                                      'templates/*.rss', ]},
      exclude_package_data={},
      test_suite = '',
      tests_require = [],
      install_requires = [])
