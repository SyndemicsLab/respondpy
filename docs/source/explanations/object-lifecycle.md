# Explanation: Object Lifecycle

This page describes the main runtime objects and how ownership flows through
the simulation assembly process.

See also:
- [How-To: Build a Single Cohort Model](../how_to/single_model_build.md)
- [References: Runtime Objects](../references/runtime_objects.md)
- [Tutorial: First End-to-End Simulation Run](../tutorials/first_run.md)

## Runtime Ownership

```mermaid
flowchart TB
	User[User code] --> In[Input]
	In --> BS[build_simulation]
	BS --> Sim[Simulation]
	BS --> BM[build_model]
	BM --> Mod[Model]
	BM --> BT[build_timestep]
	BT --> TS[Timestep]
	BT --> Tr[Transition]
	TS --> Mod
	Mod --> Sim
	Sim --> Hist[History]
```

## Class Roles

```mermaid
classDiagram
	class Input {
	  +config
	  +select_parameter()
	  +get_cohort_ids()
	}

	class Model
	class Simulation {
	  +set_duration()
	  +add_model()
	  +run()
	}
	class Timestep {
	  +add_transition()
	}
	class Transition {
	  +add_matrix()
	}
	class History

	Simulation "1" o-- "many" Model
	Model "1" o-- "many" Timestep
	Timestep "1" o-- "many" Transition
	Simulation ..> History : returns
	Input ..> Model : initial state lookup
	Input ..> Transition : parameter lookup
```

## Assembly Boundaries

```mermaid
flowchart LR
	A[Data access] --> B[Model construction]
	B --> C[Timestep assembly]
	C --> D[Transition population]
	D --> E[Simulation execution]
	E --> F[History output]
```