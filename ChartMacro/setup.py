#!/usr/bin/env python

from setuptools import find_packages, setup

version='0.1'

setup(name='ChartMacro',
      version=version,
        description = "A Trac wiki macro that shows charts on a Trac site.",
      long_description="",
        author = 'John',
    author_email = '',
    url= '',
    keywords = 'trac plugin',
    license = "",
      install_requires = [ 'Trac>=1.4.1' ],
      packages=find_packages(exclude=['ez_setup', 'examples', '*tests*']),
      include_package_data=True,
      package_data={  },
      zip_safe=True,
      entry_points={'trac.plugins': [
            'chartmacro.api = chartmacro.api'
            ]},
      classifiers=[],
      )
