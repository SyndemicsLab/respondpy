# Reference: respondpy.data

API reference for the data namespace, including input access and validation
helpers.

See also:
- [Explanation: Data Flow](../explanations/data-flow.md)
- [How-To: Load RESPOND Input Data](../how_to/load_input_data.md)
- [Tutorial: Parameter Change-Time Experiment](../tutorials/parameter_change_experiment.md)

```{automodule} respondpy.data
:members:
:undoc-members:
:show-inheritance:
```

## Public Symbols

```mermaid
classDiagram
	class ParameterType
	class Parameter
	class Input
	class build_constant_state_vector
	class build_constant_transition
	class update_retention_probability
	class verify_transition_probability
	class verify_no_nulls
	class verify_no_duplicates
	class validate_time_list

	ParameterType --> Parameter
	Parameter --> Input
	Input ..> build_constant_state_vector
	Input ..> build_constant_transition
```