# Tutorial: Interpret Model Histories

This tutorial demonstrates how to inspect model histories after a simulation
run and extract recorded timestep/state information using the history API.

See also:
- [How-To: Build and Run a Simulation](../how_to/run_simulation.md)
- [References: Runtime Objects](../references/runtime_objects.md)
- [Explanation: Runtime Execution](../explanations/runtime-execution.md)

## Step 1: Build and run a simulation subset

```python
from pathlib import Path

from respondpy.build import build_simulation
from respondpy.data import Input

input_data = Input(path=Path("/path/to/respond-input"))
subset = input_data.get_cohort_ids()[:2]

simulation = build_simulation(input_data, cohort_ids=subset)
simulation.run()
```

## Step 2: Read history names for each model

```python
for idx, model_name in enumerate(simulation.get_model_names()):
    history_names = simulation.get_model_history_names(idx)
    print(idx, model_name, history_names)
```

## Step 3: Inspect recorded timesteps and state counts

```python
model_history = simulation.get_model_history(0)

for history_name, history in model_history.items():
    timesteps = history.get_recorded_timesteps()
    states = history.get_recorded_states()
    mode = history.get_history_mode()

    print("history:", history_name)
    print("mode:", mode.name)
    print("n_timesteps:", len(timesteps))
    print("n_states:", len(states))
```

## Step 4: Access the latest recorded timestep

```python
for history_name, history in model_history.items():
    print(history_name, history.get_latest_recorded_timestep())
```

## Interpretation Flow

```mermaid
flowchart TD
	A[Simulation.run()] --> B[get_model_history(index)]
	B --> C[History objects by name]
	C --> D[get_recorded_timesteps]
	C --> E[get_recorded_states]
	C --> F[get_history_mode]
	D --> G[Temporal coverage checks]
	E --> H[State trajectory checks]
	F --> I[Snapshot vs accumulated interpretation]
```