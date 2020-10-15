# Converiting from `abcunit-cmip5-stats` to `abcunit-ncas-radar` #

|      | `abcunit-cmip5-stats`           | `abcunit-ncas-radar`                       |
| :--- | ------------------------------- | ------------------------------------------ |
| A    | `run_all.py`                    | `convert-rain-x-band-time-series.sh` |
| B    | `run_batch.py`                  | `convert-rain-x-band-day.sh`         |
| C    | `run_chunk.py`                  | `convert-rain-x-band-hour.sh`        |
| Unit | (stat, model, ensemble, var_id) | A single scan from within the hour         |

## New things for `SETTINGS.py` from `defauts.cfg` ##

* `start_date`
* `end_date`
* `CHUNK_SIZE`
* create aliases for directory paths for input data
  * RAINE_SCR_DIR=/work/scratch-nopw/lbennett/raine/
  * RAINE_GWS_DIR=$DATA_DIR/raine/cfradial/
  * CHIL_SCR_DIR=/work/scratch-nopw/lbennett/chilbolton/
  * CHIL_GWS_DIR=$DATA_DIR/chilbolton/cfradial/
  * RAINE_OBSDIR=/gws/nopw/j04/ncas_obs/amf/raw_data/ncas-mobile-x-band-radar-1/ incoming/raine
  * CHIL_OBSDIR=/gws/nopw/j04/ncas_obs/amf/raw_data/ncas-mobile-x-band-radar-1/data/chilbolton


Output directories can be formatted in the same / similar way as the original.
