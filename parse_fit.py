#!/usr/bin/env python

"""
Script to parse Garmin fit files
and extract useful information
"""

from fitparse import FitFile
import sys

fit = FitFile(sys.argv[1])

for record in fit:
    print(record)
