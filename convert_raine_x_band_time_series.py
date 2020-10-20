import argparse
from datetime import timedelta
import dateutil
import dateutil.parser as dp
import os
import SETTINGS
import subprocess

def arg_parse_all():
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """

    parser = argparse.ArgumentParser()

    type_choices = ['vol','ele','azi']

    parser.add_argument('-t', '--scan_type', nargs=1, type=str, choices=type_choices, required=True,
                        help=f'Type of scan, one of: {type_choices}', metavar='')
    parser.add_argument('-s', '--start', nargs=1, type=str, required=True, default=SETTINGS.MIN_START_DATE,
                        help=f'Start date in the format YYYYMMDD, {SETTINGS.MIN_START_DATE} at the earliest'
                        metavar='')
    parser.add_argument('-e', '--end', nargs=1, type=str, required=True, default=SETTINGS.MAX_END_DATE,
                        help=f'End date in the format YYYYMMDD, {SETTINGS.MAX_END_DATE} at the latest'
                        metavar='')

    # Not sure where to check validity of -s and -e, here or after return?  

    return parser.parse_args()

def loop_over_days(args):
    """ 
    Runs convert_rainte_x_band_day.py for each day in the given time range
    
    :param args: (namespace) Namespace object built from arguments parsed from comandline
    """

    #args.thing[0] might work and be neater
    scan_type = ''.join(args.scan_type)
    start_date = ''.join(args.start)
    end_date = ''.join(args.end)

    #validate dates
    try:
        start_date_time = dp.isoparse(start_date)
        end_date_time = dp.isoparse(end_date)
    except ValueError as err:
        print('[ERROR] Date format is incorect')
        print(err)
        exit 1 # Not sure if this is best solution

    if start_date_time > end_date_time:
        # This should be dealt with in the same way as above, whatever that becomes
        raise ValueError('Start date must be before end date')

    current_date_time = start_date_time
    current_directory = os.getcwd()

    while current_date_time <= end_date_time: # Once again to be done properly

        current_date = current_date_time.strftime("%Y%m%d")
        print(f"[INFO] Running for: {current_date}")

        cmd = f"{current_directory}/convert_raine_x_band_day.py -t {scan_type} -d {current_date}"
        print(f"[INFO] Running: {cmd}")
        subprocess.call(cmd, shell=True)

        current_date_time += timedelta(days=1)


def main():
    """Runs script if called on command line"""

    args = arg_parse_all()
    loop_over_days(args)


if __name__ == '__main__':
    main()
