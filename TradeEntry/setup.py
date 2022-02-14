# -*- coding: utf-8 -*-

from setuptools import setup

setup(name = 'Trade',
      version = '2.0',
      packages = ['trade'],
      author = 'Hobury Investments',
      author_email = '',
      keywords = 'trac trade',
      description = 'A trade entry system and trade overview within Trac',
      url = '',
      license = 'BSD',
      install_requires = ['Trac >= 1.4.1'],
      zip_safe = False,
      extras_require = {},
      entry_points = {'trac.plugins': [
          'trade.web_ui = trade.web_ui']},
      package_data = {'trade': ['htdocs/*.png',
                              'htdocs/css/*.css',
                              'htdocs/js/*.js',
                              'templates/*.html']},
      classifiers = ['Development Status :: 5 - Production/Stable', 
                     'Framework :: Trac',
                     'Programming Language :: Python'],
      exclude_package_data = {},
      test_suite = '',
      tests_require = [],
      install_requires = []
)

