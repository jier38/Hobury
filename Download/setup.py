# -*- coding: utf-8 -*-

from setuptools import setup

setup(name = 'Download',
      version = '2.0',
      packages = ['download'],
      author = 'Hobury Investments',
      author_email = '',
      keywords = 'trac download',
      description = 'A download section of company deliverables.',
      url = '',
      license = 'BSD',
      install_requires = ['Trac >= 1.4.1'],
      zip_safe = False,
      extras_require = {},
      entry_points = {'trac.plugins': [
          'download.web_ui = download.web_ui']},
      package_data={'download': ['htdocs/*.png',
                                 'htdocs/css/*.css',
                                 'htdocs/js/*.js',
                                 'templates/*.html',
                                 'templates/*.rss', ]},
      classifiers = ['Development Status :: 5 - Production/Stable', 
                     'Framework :: Trac',
                     'Programming Language :: Python'],
      exclude_package_data = {},
      test_suite = '',
      tests_require = [],
      install_requires = []
)
