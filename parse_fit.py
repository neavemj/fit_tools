#!/usr/bin/env python

"""
Script to parse Garmin fit files
and extract useful information
"""

from fitparse import FitFile
import sys
import argparse
import datetime
from tqdm import tqdm # gives a progress bar
import csv

#fit_fl = FitFile(sys.argv[1])
fit_fls = sys.argv[1:]

# use argparse to grab command line arguments

parser = argparse.ArgumentParser("parse and convert fit files into combined csv")

parser.add_argument('-f', '--fit_files', type = str,
        nargs = "+", help = "group of fit files to convert to combined csv")
parser.add_argument('-o', '--output', type = str,
        help = "output file name")

# if no args given, print help and exit

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

# check that the required arguments are provided

if args.fit_files is None or \
    args.output is None:
        print("\n** a required input is missing\n"
              "** at least one fit file and an output name is required\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

# now process fit files and extract required information

to_write = []
print("\nProcessing files.. ")
for fls in tqdm(args.fit_files):
    fit_fl = FitFile(fls)

    # session seems to be the summary of the activity
    # only problem is the timestamp is not in local time
    # however, this info is provided in the 'activity' message
    # will get both here - assuming all activities have both these fields
    try:
        for record in fit_fl.get_messages("activity"):
            activity_values = record.get_values()
            # the local time given here is recorded after the activity is finished
            # get start time by subtracting timer time
            start_time = activity_values['local_timestamp'] - datetime.timedelta(seconds = activity_values['total_timer_time'])
            start_date = start_time.strftime("%Y-%m-%d %H:%M:%S")
    except:
        print("data could not be retrieved from file: {}".format(fls))
        continue

    for record in fit_fl.get_messages("session"):
        # get a dictionary of data in this record
        values = record.get_values()
        # extract specific things from this file to write out
        to_write.append([
            values['sport'],
            values['timestamp'],
            start_date,
            values['total_elapsed_time'],
            values['total_timer_time'],
            values['total_distance'],
            values['avg_speed'],
            values['avg_heart_rate'],
            values['max_heart_rate'],
            ])

# now write the list of lists to a csv file
with open(args.output, "w") as f:
    writer = csv.writer(f)
    writer.writerow(['sport', 'timestamp', 'local_date', 'total_elapsed_time',
        'total_timer_time', 'total_distance', 'avg_speed', 'avg_heart_rate', 'max_heart_rate'])
    writer.writerows(to_write)
