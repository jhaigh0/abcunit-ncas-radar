import argparse
import dateutil
import dateutil.parser as dp
import os
import SETTINGS
import subprocess

def arg_parse_hour():
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """

    parser = argparse.ArgumentParser()
    type_choices = ['vol','ele','azi']

    parser.add_argument('-t', '--scan_type',  nargs=1, type=str, choices=type_choices, required=True,
                        help=f'Type of scan, one of: {type_choices}', metavar='')
    # Not sure if this will work along side having a tagged parameter
    parser.add_argument('hours', nargs='?', type=str, required=True, help='The hours you want to run'
                        'in the format YYYYMMDDHH', metavar='')

    # Getting the dates could be done with sys.argv[3:], seems like
    # we should be able to use argparse to do it in a smarter

    return parser.parse_args()


def loop_over_hours(args):

    scan_type = ''.join(args.scan_type)
    hours = args.hours

    date = dp.isoparse(hours[0][:-2])
    year = date.year
    month = date.month
    day = date.day
    # Above to be used for output paths I think

    failure_count = 0

    # Mapping scan type bit goes here, separate script / method
    mapped_scan_type = ''

    for hour in hours:

        print(f'[INFO] Processing: {hour}')

        # Get input files with another script / method
        input_files = []

        for dbz_file in input_files:

            if failure_count >= SETTINGS.EXIT_AFTER_N_FAILURES:
                print('[WARN] Exiting after failure count reaches limit: '
                      f'{SETTINGS.EXIT_AFTER_N_FAILURES}')
                exit 1 # Could raise something instead of all this
            
            # File and output setup goes here

            # Check if allready successful

            # Remove eroneous runs

            # 'Get expected variables as a single space-delimited string' set expected_vars
            expected_vars = []

            # 'Process the uncalibrated data' (where output is generated)

            # Check for expected netcdf output

            # Get found_vars from the nc file (probably can use a nice library)
            found_vars = []

            print('[INFO] Checking that the output variables match those in the input files')

            if found_vars != expected_vars:
                print('[ERROR] Output variables are not the same as input files'
                      f'{found_vars} != {expected_vars}')
                failure_count += 1
                # create error output bad_num
            else:
                print(f'[INFO] All expected variable were found: {expected_vars}') 

            #output a success

def main():
    """Runs script if called on command line"""

    args = arg_parse_hour()
    loop_over_hours(args)


if __name__ == '__main__':
    main()