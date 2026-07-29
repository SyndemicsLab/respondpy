# Explanation: Public API

This page summarizes the top-level modules and classes that make up the
library surface exposed by `respondpy`.

See also:
- [How-To Guides](../how_to/data_loading.md)
- [References](../references/wrapper_typing.md)
- [Tutorials](../tutorials/base_respond.md)

## Package Surface

```mermaid
flowchart LR
	subgraph respondpy
		data[data]
		cost_effectiveness[cost_effectiveness]
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

	data --> data_api[data API]
	cost_effectiveness --> cost_api[discount, cwise_product, cwise_min, calculate_life_years]
	build_simulation --> Simulation
	build_model --> Model
	build_timestep --> Timestep
	build_default_transitions --> Transition
	build_transition --> Transition
	add_matrix_to_transition --> Transition
```

## Data Namespace

```mermaid
flowchart TB
	subgraph respondpy.data
		ParameterType[ParameterType]
		Parameter[Parameter]
		Input[Input]
		build_constant_state_vector[build_constant_state_vector]
		build_constant_transition[build_constant_transition]
		update_retention_probability[update_retention_probability]
		verify_transition_probability[verify_transition_probability]
		verify_no_nulls[verify_no_nulls]
		verify_no_duplicates[verify_no_duplicates]
		validate_time_list[validate_time_list]
	end

	ParameterType --> Parameter
	Parameter --> Input
	Parameter --> build_constant_transition
	Parameter --> build_constant_state_vector
	Parameter --> update_retention_probability
	Parameter --> validate_time_list
```

## Public Classes

```mermaid
classDiagram
	class Input
	class Model
	class Simulation
	class Timestep
	class Transition
	class History

	Simulation "1" o-- "many" Model
	Model "1" o-- "many" Timestep
	Timestep "1" o-- "many" Transition
	Simulation ..> History : produces
	Input ..> Model : supplies state data
	Input ..> Transition : supplies matrices
```