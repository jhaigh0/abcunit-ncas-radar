import argparse
from datetime import timedelta
import dateutil
import dateutil.parser as dp
import os
import SETTINGS
import subprocess

def arg_parse_day():
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """

    parser = argparse.ArgumentParser()
    type_choices = ['vol','ele','azi']

    parser.add_argument('-t', '--scan_type', nargs=1, type=str, choices=type_choices, required=True,
                        help=f'Type of scan, one of: {type_choices}', metavar='')
    parser.add_argument('-d', '--date', nargs=1, type=str, required=True
                        help=f'Date to find scans from, fromat YYYYMMDD, between '
                        f'{SETTINGS.MIN_START_DATE} and {SETTINGS.MAX_END_DATE}', metavar='')
    
    return parser.parse_args()

def loop_over_chunks(args):
    """
    Loops through a day in hour chunks of size SETTINGS.CHUNK_SIZE and submits
    those times to convert_raine_x_band_hour.py
    
    :param args: (namespace) Namespace object built from attributes parsed from command line
    """

    scan_type = ''.join(args.scan_type)
    date = ''.join(arg.date)

    day_date_time = dp.isoparse(date)
    min_date = dp.isoparse(SETTINGS.MIN_START_DATE)
    max_date = dp.isoparse(SETTINGS.MAX_END_DATE)

    if day_date_time < min_date or day_date_time > max_date:
        raise ValueError(f'Date must be in range {SETTINGS.MIN_START_DATE} - {SETTINGS.MAX_END_DATE}')

    n_chunks = 24 / SETTINGS.CHUNK_SIZE # Division is weird, check this is the best way

    if n_chunks < 1:
        raise ValueError('SETTINGS.CHUNK_SIZE must be 24 or less')

    # This is the point output dirs start to get setup
    # Leaving for now to think about how backend would work

    start_day = day_date_time.day
    current_day_date_time = day_date_time

    # Not sure this makes sense for chunk sizes which don't go nicely into 24,
    # but it's equivelant to the original.
    while current_day_date_time.day = start_day: 

        hours = []
        current_directory = os.getcwd()

        # Hour has to be formatted properly 
        for hour in [current_day_date_time + timedelta(hours=x) for x in range(SETTINGS.CHUNK_SIZE)]
            hour_str = hour.strftime("%Y%m%d%H")
            hours.append(hour_str) 

        #incement current_day_date_time somehow
        current_day_date_time += timedelta(hours=SETTINGS.CHUNK_SIZE)

        print(f"[INFO] Running for {hours}")

        wallclock = f"{SETTINGS.CHUNK_SIZE / 2}:00" #this needs to be integer division

        slurm_command = f"sbatch -p {SETTINGS.QUEUE} -t {wallclock} -o something " \
                        f"-e something {current_directory}/convert_raine_x_band_hour.py " \
                        f"-t {scan_type} {' '.join(hours)}"
        print(f"[INFO] Running: {slurm_command}")
        subprocess.call(slurm_command, shell=True)


def main():
    """Runs script if called on command line"""

    args = arg_parse_day()
    loop_over_chunks(args)


if __name__ == '__main__':
    main()