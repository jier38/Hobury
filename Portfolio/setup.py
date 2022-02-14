# -*- coding: utf-8 -*-

from setuptools import setup

setup(name = 'Portfolio',
      version = '2.0',
      packages = ['portfolio'],
      author = 'Hobury Investments',
      author_email = '',
      keywords = 'trac portfolio',
      description = 'Create, update and delete portfolios for trade management purposes',
      url = '',
      license = 'BSD',
      install_requires = ['Trac >= 1.4.1'],
      zip_safe = False,
      extras_require = {},
      entry_points = {'trac.plugins': [
          'portfolio.admin = portfolio.admin']},
      package_data = {'portfolio': ['htdocs/*.png',
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
