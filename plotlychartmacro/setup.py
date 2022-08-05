#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup (
    name = 'PlotlyChart',
    version = 0.1,
    license = 'BSD',
    description = 'Provides plotly based charts.',
    packages = find_packages(exclude=['*.tests']),
    package_data = { 'plotlychart': ['htdocs/*.png','htdocs/*.js',
        'htdocs/*.css', 'htdocs/ployly/*.js', 'htdocs/plotly/plugins/*.js',
        'htdocs/plotly/*.css'] },
    entry_points = {'trac.plugins': ['PlotlyChart = plotlychart.macro']},
    keywords = 'trac macro',
)
