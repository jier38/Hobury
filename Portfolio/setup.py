# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='Portfolio',
      version='2.0',
      packages=['portfolio'],
      author='Hobury Investments',
      author_email='',
      keywords='trac portfolio',
      description='',
      url='',
      license='BSD',
      zip_safe=False,
      extras_require={},
      entry_points={'trac.plugins': [
          'portfolio.admin = portfolio.admin']},
      package_data={'portfolio': ['htdocs/*.png',
                                  'htdocs/css/*.css',
                                  'htdocs/js/*.js',
                                  'templates/*.html',
                                  'templates/*.rss', ]},
      exclude_package_data={},
      test_suite='',
      tests_require=[],
      install_requires=[])
