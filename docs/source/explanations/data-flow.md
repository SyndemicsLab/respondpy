# Explanation: Data Flow

This page follows the path from persisted RESPOND inputs to model-ready arrays
and transition matrices.

See also:
- [How-To: Load RESPOND Input Data](../how_to/load_input_data.md)
- [References: respondpy.data](../references/data.md)
- [Tutorial: Parameter Change-Time Experiment](../tutorials/parameter_change_experiment.md)

## Input Processing

```mermaid
flowchart LR
	A[SQLite database] --> B[Input]
	C[sim.conf] --> B
	B --> D[Parameter]
	D --> E[select_parameter]
	E --> F[Raw rows or numpy arrays]
```

## Parameter Mapping

```mermaid
flowchart TB
	A[ParameterType]
	A --> B[INITIAL_COHORT]
	A --> C[MIGRATION_COHORT]
	A --> D[INTERVENTION_TRANSITION_PROBABILITY]
	A --> E[BEHAVIOR_TRANSITION_PROBABILITY]
	A --> F[OVERDOSE_PROBABILITY]
	A --> G[OVERDOSE_FATALITY_PROBABILITY]
	A --> H[BACKGROUND_DEATH_PROBABILITY]
	A --> I[STANDARD_MORTALITY_RATIO]

	D --> J[transition matrix columns]
	E --> J
	F --> K[probability column]
	G --> K
	H --> K
	I --> L[ratio column]
	B --> M[count column]
	C --> M
```

## Validation and Normalization

```mermaid
flowchart LR
	A[change-time values] --> B[validate_time_list]
	B --> C[normalized ascending times]
	D[transition rows] --> E[verify_no_nulls]
	D --> F[verify_no_duplicates]
	D --> G[update_retention_probability]
	G --> H[normalized transitions]
```