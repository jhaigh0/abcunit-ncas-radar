EXIT_AFTER_N_FAILURES = 1000000

MIN_START_DATE = '20181025'
MAX_END_DATE = '20200331'

# lotus settings
QUEUE = 'short-serial'
CHUNK_SIZE = 6 # in hours

### Output path templates ###

#Copied from the original defaults.cfg, probably needs changing
LOTUS_OUTPUTS_BASEDIR = "/home/users/lbennett/logs/lotus-output"
LOG_BASEDIR = "/home/users/lbennett/logs"

PARAMS_FILE_RAINE = "/home/users/lbennett/lrose/ingest_params/RadxConvert.raine.uncalib.test"
PARAMS_FILE = "/home/users/lbennett/lrose/ingest_params/RadxConvert.chilbolton.uncalib"
#

#staying here for now
LOTUS_OUTPUT_PATH_TMPL = "{current_directory}/logs/lotus_outputs/{stat}/{model}"
OUTPUT_PATH_TMPL = "{GWS}/{USER}/abcunit-outputs"
SUCCESS_DIR = "{current_directory}/logs/success"
FAILURE_DIR = "{current_directory}/logs/failure"

# choice for output handling
BACKEND = 'db' #'db' or 'file'

## More directories ##

#Copied from the set_up.sh scripts
DATA_DIR = "/gws/nopw/j04/ncas_radar_vol2/data/xband"
RAINE_DIR = "/gws/nopw/j04/ncas_obs/amf/raw_data/ncas-mobile-x-band-radar-1/incoming/raine"
CHIL_DIR = "/gws/nopw/j04/ncas_obs/amf/raw_data/ncas-mobile-x-band-radar-1/data/chilbolton"

