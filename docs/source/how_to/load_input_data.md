# How-To: Load RESPOND Input Data

Use this guide to initialize an `Input` object from RESPOND database and
configuration files.

See also:
- [Tutorial: First End-to-End Simulation Run](../tutorials/first_run.md)
- [References: respondpy.data](../references/data.md)
- [Explanation: Data Flow](../explanations/data-flow.md)

## Load from a shared directory

```python
from pathlib import Path

from respondpy.data import Input

base_path = Path("/path/to/respond-input")
input_data = Input(path=base_path)

print(input_data)
print(input_data.get_cohort_ids())
```

## Load from explicit file paths

```python
from pathlib import Path

from respondpy.data import Input

db_file = Path("/path/to/respond-input/input.db")
conf_file = Path("/path/to/respond-input/sim.conf")

input_data = Input(db_path=db_file, conf_path=conf_file)

duration = int(input_data.config.get("simulation", "duration"))
print(duration)
```

## Verify required simulation config values

```python
from pathlib import Path

from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))

duration = input_data.config.get("simulation", "duration")
change_times = input_data.config.get("simulation", "parameter_change_times")

print("duration:", duration)
print("parameter_change_times:", change_times)
```