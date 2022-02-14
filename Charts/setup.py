# -*- coding: utf-8 -*-

from setuptools import setup

setup(name = 'Charts',
      version = '1.0',
      packages = ['charts'],
      author = 'Hobury Investments',
      author_email = '',
      keywords = 'trac charts',
      description = 'Display dynamically created charts on Trac pages',
      url = '',
      license = 'BSD',
      install_requires = ['Trac >= 1.4.1'],
      zip_safe = False,
      extras_require = {},
      entry_points = {'trac.plugins': [
          'charts.web_ui = charts.web_ui']},
      package_data = {'charts': ['htdocs/*.*', 'templates/*.*']},
      classifiers = ['Development Status :: 5 - Production/Stable', 
                     'Framework :: Trac',
                     'Programming Language :: Python'],
      exclude_package_data = {},
      test_suite = '',
      tests_require = [],
      install_requires = []
)
