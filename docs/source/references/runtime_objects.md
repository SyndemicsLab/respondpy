# Reference: Runtime Objects

API reference for runtime classes exposed through the core wrapper modules.

See also:
- [Explanation: Object Lifecycle](../explanations/object-lifecycle.md)
- [How-To: Build a Single Cohort Model](../how_to/single_model_build.md)
- [Tutorial: Interpret Model Histories](../tutorials/history_interpretation.md)

```{automodule} respondpy.history
:members:
:undoc-members:
:show-inheritance:
```

```{automodule} respondpy.model
:members:
:undoc-members:
:show-inheritance:
```

```{automodule} respondpy.simulation
:members:
:undoc-members:
:show-inheritance:
```

```{automodule} respondpy.timestep
:members:
:undoc-members:
:show-inheritance:
```

```{automodule} respondpy.transition
:members:
:undoc-members:
:show-inheritance:
```

## Runtime Graph

```mermaid
classDiagram
	class Input
	class History
	class Model
	class Simulation
	class Timestep
	class Transition

	Simulation "1" o-- "many" Model
	Model "1" o-- "many" Timestep
	Timestep "1" o-- "many" Transition
	Simulation ..> History : produces
	Input ..> Model : initializes
	Input ..> Transition : populates
```