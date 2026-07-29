# How-To: Build and Run a Simulation

Use this guide when you want the shortest path from RESPOND input files to a
simulation run with history outputs.

See also:
- [Tutorial: First End-to-End Simulation Run](../tutorials/first_run.md)
- [References: respondpy.build](../references/build.md)
- [Explanation: Runtime Execution](../explanations/runtime-execution.md)

## Build and run all cohorts

```python
from pathlib import Path

from respondpy.build import build_simulation
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))

simulation = build_simulation(input_data)
simulation.run()

model_names = simulation.get_model_names()
print(len(model_names))
```

## Build and run selected cohorts

```python
from pathlib import Path

from respondpy.build import build_simulation
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))

simulation = build_simulation(input_data, cohort_ids=[1, 3, 5])
simulation.run()

for idx, _ in enumerate(simulation.get_model_names()):
    history_names = simulation.get_model_history_names(idx)
    print(history_names)
```

## Use run-specific logging

```python
from pathlib import Path

from respondpy.build import build_simulation
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))

simulation = build_simulation(
    input_data,
    log_name="respond_embed",
    log_file="respond_embed.log",
)
simulation.run()
```