# Architecture

This section explains the public API and runtime behavior of respondpy.
It is intentionally conceptual: there are no references pages here and no
how-to recipes.

If you need task-oriented steps, use [How-To Guides](../how_to/data_loading.md).
If you need API signatures and symbol-level details, use
[References](../references/wrapper_typing.md).
If you want guided learning exercises, use
[Tutorials](../tutorials/base_respond.md).

```{toctree}
:maxdepth: 1

public-api
object-lifecycle
data-flow
runtime-execution
```

## Overview

```mermaid
flowchart LR
	subgraph Public[respondpy public surface]
		data[data]
		cost[cost_effectiveness]
		History[History]
		Model[Model]
		Simulation[Simulation]
		Timestep[Timestep]
		Transition[Transition]
		build_simulation[build_simulation]
		build_model[build_model]
		build_timestep[build_timestep]
		build_default_transitions[build_default_transitions]
		build_transition[build_transition]
		add_matrix_to_transition[add_matrix_to_transition]
	end

	build_simulation --> Simulation
	build_model --> Model
	build_timestep --> Timestep
	build_default_transitions --> Transition
	build_transition --> Transition
	add_matrix_to_transition --> Transition
	Simulation --> History
	data --> Model
	data --> Transition
```

## Scope

```mermaid
flowchart TB
	A[Public API]
	B[Core runtime objects]
	C[Data access and validation]
	D[Simulation assembly helpers]
	E[Execution and output flow]

	A --> B
	A --> C
	A --> D
	A --> E
```
