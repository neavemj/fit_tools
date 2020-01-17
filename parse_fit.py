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
        #print(values)
        #{'timestamp': datetime.datetime(2018, 2, 7, 20, 32, 26), 'start_time': datetime.datetime(2018, 2, 7, 20, 18, 31), 'start_position_lat': -456730065, 'start_position_long': 1723890224, 'total_elapsed_time': 423.883, 'total_timer_time': 423.883, 'total_distance': 538.46, 'total_cycles': 99, 'unknown_78': None, 'message_index': 0, 'total_calories': 24, 'enhanced_avg_speed': 1.27, 'avg_speed': 1270, 'first_lap_index': 0, 'num_laps': 1, 'unknown_33': None, 'num_active_lengths': None, 'event': 'lap', 'event_type': 'stop', 'sport': 'generic', 'sub_sport': 'generic', 'avg_heart_rate': 77, 'max_heart_rate': 88, 'avg_cadence': 51, 'max_cadence': 59, 'trigger': 'activity_end'}
        #The 'enhanced' fields were added to allow expressing speeds/altitudes too large for the existing 16bit fields. They are likely of limited interest to (most) human powered activities.
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
            values['total_calories'],
            ])

# now write the list of lists to a csv file
with open(args.output, "w") as f:
    writer = csv.writer(f)
    writer.writerow(['sport', 'timestamp', 'local_date', 'total_elapsed_time',
        'total_timer_time', 'total_distance', 'avg_speed', 'avg_heart_rate',
        'max_heart_rate', 'calories'])
    writer.writerows(to_write)
