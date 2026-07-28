# Explanation: Runtime Execution

This page shows the construction and execution sequence of a simulation run.

See also:
- [How-To: Build and Run a Simulation](../how_to/run_simulation.md)
- [References: respondpy.build](../references/build.md)
- [Tutorial: First End-to-End Simulation Run](../tutorials/first_run.md)

## Build Sequence

```mermaid
sequenceDiagram
	autonumber
	actor User
	participant In as Input
	participant BS as build_simulation()
	participant BM as build_model()
	participant BT as build_timestep()
	participant BDT as build_default_transitions()
	participant Tr as Transition
	participant TS as Timestep
	participant Mod as Model
	participant Sim as Simulation

	User->>In: create Input(path or db/config files)
	User->>BS: build_simulation(In, cohort_ids)
	loop each cohort id
		BS->>BM: build_model(In, cohort_id)
		BM->>In: select_parameter(INITIAL_COHORT, cohort_id, time=1)
		BM->>Mod: set_state(initial_state)
		loop each model timestep
			BM->>BT: build_timestep(In, cohort_id, tstep)
			BT->>BDT: build_default_transitions(In, cohort_id, time=tstep)
			BDT-->>BT: migration, behavior, intervention, overdose, mortality
			BT->>TS: add_transition(Transition)
			TS-->>BM: timestep
		end
		BS->>Sim: add_model(Model)
	end
```

## Execution Sequence

```mermaid
sequenceDiagram
	autonumber
	actor User
	participant Sim as Simulation
	participant Mod as Model
	participant TS as Timestep
	participant Tr as Transition
	participant Hist as History

	User->>Sim: run()
	loop for each model
		Sim->>Mod: advance state over time
		loop for each timestep
			Mod->>TS: apply transitions
			loop for each transition
				TS->>Tr: evaluate matrix
			end
		end
		Sim->>Hist: collect sparse history
	end
	User->>Sim: get_model_history(index)
	Sim-->>User: mapping of history names to History objects
```