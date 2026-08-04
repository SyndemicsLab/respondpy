# How-To: Select Cohorts and Configure Logging

Use this guide to scope a run to a cohort subset and set deterministic logging
settings for embedded workflows.

See also:
- [How-To: Build and Run a Simulation](run_simulation.md)
- [Tutorial: First End-to-End Simulation Run](../tutorials/first_run.md)
- [References: respondpy.build](../references/build.md)

## Discover valid cohort IDs

```python
from pathlib import Path

from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))
cohort_ids = input_data.get_cohort_ids()

print(cohort_ids)
```

## Build a subset simulation safely

```python
from pathlib import Path

from respondpy.build import build_simulation
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))

target_cohorts = [cohort_id for cohort_id in input_data.get_cohort_ids()[:2]]

simulation = build_simulation(
    input_data,
    cohort_ids=target_cohorts,
    log_name="respond_subset",
    log_file="respond_subset.log",
)

simulation.run()
print(len(simulation.get_model_names()))
```

## Write Python logs to the same RESPOND log file

```python
from pathlib import Path

import respondpy as rpy
from respondpy.build import build_simulation
from respondpy.data import Input

input_data = Input(
    path=Path("/path/to/respond-input"),
    log_name="respond",
    log_file="respond.log",
)

simulation = build_simulation(
    input_data,
    log_name="respond",
    log_file="respond.log",
)

rpy.logging.log_info("respond", "Starting simulation run from Python")
simulation.run()
rpy.logging.log_info("respond", "Simulation run complete")
rpy.logging.flush_all_loggers()
```

For concurrent logging to one file, use shared sink helpers before creating
runtime objects:

```python
import respondpy as rpy

rpy.logging.create_shared_file_sink("respond.log")
rpy.logging.create_shared_logger("respond")
```

## Fail fast on unknown cohorts

```python
from pathlib import Path

from respondpy.build import build_simulation
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))

try:
    build_simulation(input_data, cohort_ids=[999999])
except ValueError as exc:
    print(exc)
```