#!/usr/bin/env python

"""
Script to parse Garmin fit files
and extract useful information
"""

from fitparse import FitFile
import sys
import time

#fit_fl = FitFile(sys.argv[1])
fit_fls = sys.argv[1:]

for fls in fit_fls:
    fit_fl = FitFile(fls)

    for record in fit_fl.get_messages("sport"):
        print("new_record")
        values = record.get_values()
        print(values)
        print("\n")
        break



#ts = values["local_timestamp"]
#print(ts.strftime("%Y-%m-%d %H:%M:%S"))
