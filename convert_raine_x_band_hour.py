import argparse
import dateutil
import dateutil.parser as dp
import os
from .output_handler.database_handler import DataBaseHandler
from .output_handler.file_system_handler import FileSystemHandler
import re
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

def map_scan_type(type):

    scan_dict = {
        'vol': 'SUR',
        'ele': 'RHI',
        'azi': 'VER',
        'SUR': 'vol',
        'RHI': 'ele',
        'VER': 'azi'
    }

    if type in scan_dict:
        return scan_dict[type]
    
    raise KeyError(f'Cannot match scan type {type}')

def get_input_files(hour, scan_type):

    # Probably needs a try round it to format check
    date_dir = dp.isoparse(hour[:-2]).strftime("%Y-%m-%d")

    # IMPORTANT this path needs to be formatted so we can choose between cihlbolton and raine 
    # (although /raine doesn't have anything in it at the moment)
    files_path = '/gws/nopw/j04/ncas_obs/amf/raw_data/ncas-mobile-x-band-radar-1/data/chilbolton'
    # They're all dirs but feels good to check
    dirs = [[name for name in os.listdir(files_path) if os.path.isdir(os.path.join(files_path, name))]] 

    # IMPORTANT this is just coppied from get-input-files.sh, shouldn't always be chilbolton
    if scan_type == 'vol':
        pattern = re.compile("^chilbolton.*_.*.vol")
    elif scan_type == 'ele':
        pattern = re.compile("^chilbolton_.*.ele")
    elif scan_type == 'azi':
        pattern = re.compile("^chilbolton.*.azi")

    return [name for name in dirs if pattern.match(name)].sort()

def _get_results_handler(n_facests, sep, error_types):

    if SETTINGS.BACKEND == 'db':
        constring = os.environ.get("ABCUNIT_DB_SETTINGS")
        if not constring:
            raise KeyError('Please create environment variable ABCUNI_DB_SETTINGS'
                            'in for format of "dbname=<db_name> user=<user_name>'
                            'host=<host_name> password=<password>"')
        return DataBaseHandler(constring, error_types)
    elif SETTINGS.BACKEND == 'file':
        return FileSystemHandler(n_facets, sep, error_types)
    else:
        raise ValueError('SETTINGS.BACKEND is not set properly')

def loop_over_hours(args):

    scan_type = ''.join(args.scan_type)
    hours = args.hours

    date = dp.isoparse(hours[0][:-2])
    year = date.year
    month = date.month
    day = date.day
    
    # THIS IS ALL TO CHANGE
    rh = _get_results_handler(4,'.',['bad_num', 'failure'])

    failure_count = 0

    mapped_scan_type = map_scan_type(scan_type)

    for hour in hours:

        print(f'[INFO] Processing: {hour}')

        # Get input files with another script / method
        input_files = get_input_files(hour, scan_type)

        # The word file feels a bit misleading since they're directories
        for dbz_file in input_files:

            if failure_count >= SETTINGS.EXIT_AFTER_N_FAILURES:
                print('[WARN] Exiting after failure count reaches limit: '
                      f'{SETTINGS.EXIT_AFTER_N_FAILURES}')
                exit 1 # Could raise something instead of all this
            
            # File and output setup goes here
            identifier = f'{year}.{month}.{day}.{os.path.splittext(dbz_file)[0]}'

            # Check if allready successful
            if rh.ran_succesfully(identifier):
                print(f'[INFO] Already ran {dbz_file} sucessfully')
                continue

            # Remove eroneous runs
            rh.delete_result(identifier)

            # 'Get expected variables as a single space-delimited string' set expected_vars
            expected_vars = []

            # 'Process the uncalibrated data' (where output is generated)
            script_cmd = f"RadxConvert -v -params {SETTINGS.PARAMS_FILE_RAINE} -f {dbz_file}"
            print(f'[INFO] Running: {script_cmd}')
            subprocess.call(script_cmd, shell=True)

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