# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='Charts',
      version='1.0',
      packages=['charts'],
      author='Hobury Investments',
      author_email='',
      keywords='trac charts',
      description='',
      url='',
      license='BSD',
      zip_safe=False,
      extras_require={},
      entry_points={'trac.plugins': [
          'charts.web_ui = charts.web_ui']},
      package_data={'charts': ['htdocs/*.*', 'templates/*.*']},
      exclude_package_data={},
      test_suite='',
      tests_require=[],
      install_requires=[])
