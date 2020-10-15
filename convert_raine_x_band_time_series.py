import argparse
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
    start_date_time = start_date # To be replaced with proper paresing
    end_date_time = end_date     # Can put in try / error check for format 

    if start_date_time > end_date_time:
        raise ValueError('Start date but be before end date')

    current_date_time = start_date_time
    current_directory = os.getcwd()

    while current_date_time <= end_date_time: # Once again to be done properly

        print(f"[INFO] Running for: {current_date_time}")

        cmd = f"{current_directory}/convert_raine_x_band_day.py -t {scan_type} -d {current_date_time}"
        print(f"[INFO] Running: {cmd}")
        subprocess.call(cmd, shell=True)

        current_date_time += 1 # add a day

def main():
    """Runs script if called on command line"""

    args = arg_parse_all()
    loop_over_days(args)

    


if __name__ == '__main__':
    main()