# Converiting from `abcunit-cmip5-stats` to `abcunit-ncas-radar` #

|      | `abcunit-cmip5-stats`           | `abcunit-ncas-radar`                       |
| :--- | ------------------------------- | ------------------------------------------ |
| A    | `run_all.py`                    | `convert-chilbolton-x-band-time-series.sh` |
| B    | `run_batch.py`                  | `convert-chilbolton-x-band-day.sh`         |
| C    | `run_chunk.py`                  | `convert-chilbolton-x-band-hour.sh`        |
| Unit | (stat, model, ensemble, var_id) | A single scan from within the hour         |

