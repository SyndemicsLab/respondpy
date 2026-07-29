# How-To: Build a Single Cohort Model

Use this guide when you need to inspect one cohort model before integrating it
into a multi-cohort simulation run.

See also:
- [How-To: Build and Run a Simulation](run_simulation.md)
- [References: Runtime Objects](../references/runtime_objects.md)
- [Explanation: Object Lifecycle](../explanations/object-lifecycle.md)

## Build one model from input data

```python
from pathlib import Path

from respondpy.build import build_model
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))

cohort_id = input_data.get_cohort_ids()[0]
model = build_model(input_data, cohort_id)

print(type(model).__name__)
```

## Build one timestep explicitly

```python
from pathlib import Path

from respondpy.build import build_timestep
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))
cohort_id = input_data.get_cohort_ids()[0]

timestep = build_timestep(input_data, cohort_id, tstep=1)
print(type(timestep).__name__)
```

## Build default transitions for a time point

```python
from pathlib import Path

from respondpy.build import build_default_transitions
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))
cohort_id = input_data.get_cohort_ids()[0]

transitions = build_default_transitions(input_data, cohort_id, time=1)
print([type(t).__name__ for t in transitions])
```