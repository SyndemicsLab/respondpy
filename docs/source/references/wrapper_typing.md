# References

This section contains technical reference material for the public API and
runtime-facing modules exposed by respondpy.

The package ships typing declarations for the native runtime classes and
their Python facades. The runtime-config constructors and simulation accessors
are typed with `RuntimeConfig` and `ExecutionConfig`; logging functions use
the `LoggingConfig`, `CreationStatus`, `LogType`, and `LogPattern` types from
`respondpy.logging`.

Runtime objects use `RuntimeConfig` and `LoggingConfig` for execution and
logging settings; deprecated logger-string overloads are not exposed.

For conceptual architecture and execution behavior, use
[Explanations](../explanations/architecture.md).
For operational workflows, use [How-To Guides](../how_to/data_loading.md).
For stepwise onboarding exercises, use [Tutorials](../tutorials/base_respond.md).

```{toctree}
:maxdepth: 1

package
logging
data
build
cost_effectiveness
runtime_objects
```

## Scope

```mermaid
flowchart LR
	A[respondpy package] --> B[Package reference]
	A --> C[data namespace]
	A --> D[build helpers]
	A --> E[cost_effectiveness]
	A --> F[runtime objects]
```
