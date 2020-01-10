#!/usr/bin/env python

"""
Script to parse Garmin fit files
and extract useful information
"""

from fitparse import FitFile
import sys
import datetime

#fit_fl = FitFile(sys.argv[1])
fit_fls = sys.argv[1:]

for fls in fit_fls:
    fit_fl = FitFile(fls)

    # session seems to be the summary of the activity
    # only problem is the timestamp is not in local time
    # however, this info is provided in the 'activity' message
    # will get both here - assuming all activities have both these fields
    for record in fit_fl.get_messages("session"):
        print("new_activity")
        values = record.get_values()
        print(values)

    for record in fit_fl.get_messages("activity"):
        values = record.get_values()
        print(values)
        # the local time given here is recorded after the activity is finished
        # get start time by subtracting timer time?
        start_time = values['local_timestamp'] - datetime.timedelta(seconds = values['total_timer_time'])
        print("started:", start_time)
        print("\n")



#ts = values["local_timestamp"]
#print(ts.strftime("%Y-%m-%d %H:%M:%S"))
