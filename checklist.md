I would not declare `v1.0.0` yet. The package works, but several parts of the release contract are still implicit.

**Review Checkpoint: API Stabilization (2026-10-07)**

This is an intentional review point. The current scope is ready for review and
should not be expanded until feedback is addressed.

Completed in this scope:

- Public runtime/stub parity for model, simulation, timestep, transition, and history changes.
- Clone ownership and Python negative-index semantics.
- State-vector shape normalization for `(m,)`, `(m, 1)`, and `(1, m)`.
- `Model.to_json()` inspection snapshots and removal of the unusable Python `serialize()` binding.
- `Input.close()` and context-manager lifecycle support.
- Simulation configuration validation and RESPOND SQLite table/column validation.
- Documentation, regression tests, and a full-suite result of `167 passed`.

Deferred until after review:

- Release metadata and supported platform/version matrix.
- Artifact-level wheel and sdist testing.
- Native dependency pinning.
- Broader scientific and numerical regression coverage.
- Threading, schema-version, and compatibility policy documentation.

**Release blockers**

1. **Freeze and document the public API**

   Runtime bindings, Python facades, `.pyi` files, and documentation need to agree. The stable v1 JSON snapshot is exposed as `Model.to_json()`; native diagnostic serialization is not part of the Python API.

2. **Resolve release metadata**

   `pyproject.toml:7-34` still declares:

   - Version `0.3.3`
   - `Development Status :: 3 - Alpha`
   - Python 3.10 classifier despite requiring Python `>=3.11`

   A v1 release needs a single authoritative version and support matrix.

3. **Define the platform promise**

   CI tests Linux, Windows, and macOS, while wheel builds target Linux and Windows in `deploy.yml:10-21`. Decide explicitly:

   - Which operating systems are supported.
   - Which Python versions are supported.
   - Which architectures are supported.
   - Whether macOS is unsupported or simply not yet published.

   Then make README, classifiers, CI, and released artifacts agree.

4. **Add artifact-level release testing**

   The release workflow should build wheels and an sdist, then install and test those actual artifacts. It should verify:

   - Importing the installed package.
   - Runtime bindings.
   - `.pyi` typing checks.
   - Representative SQLite-backed simulations.
   - Every supported Python/platform combination.

   Current cibuildwheel testing skips Python 3.13 and 3.14 in `pyproject.toml:245-252`, so those builds are not fully validated.

5. **Make native builds reproducible**

   `CMakeLists.txt:54-65` fetches `spdlog` from the floating `v1.x` branch. Pin it to an exact commit or release. The C++ RESPOND dependency is pinned, which is good; all native dependencies should follow the same rule.

**Important before v1**

6. **Specify the SQLite/configuration contract**

   `Input` hard-codes table names, columns, and configuration keys in `input.py:20-105`. Remaining work is:

   - [x] Required tables and columns.
   - [x] Required config sections and keys.
   - Supported schema versions.
   - Compatibility with the canonical RESPONDv2 input database.
   - [x] Clear package-level errors for invalid inputs.

7. **Strengthen numerical regression coverage**

   Add reference-based tests for:

   - Population conservation.
   - Transition probability normalization.
   - Mortality and overdose ordering.
   - Multiple intervention and behavior dimensions.
   - Time-varying parameters.
   - Missing, duplicate, invalid, NaN, and infinite values.
   - Deterministic repeated runs.

   For a scientific simulation package, these are more important than ordinary line coverage.

8. **Clarify resource and threading behavior**

   `Input` owns a SQLite connection and now has documented `close()` and context-manager support. Document whether an `Input` instance may be shared across threads. Also specify how global logging behaves when multiple simulations run concurrently.

9. **Improve error contracts**

   Validate arguments such as negative processor counts, invalid durations, invalid timestep lists, and malformed configuration values. Prefer documented exception types and messages instead of exposing raw `ConfigParser`, SQLite, or C++ errors.

10. **Finish the documentation transition**

    `index.rst:10-14` still says the API may change. That is appropriate pre-1.0, but should be replaced with a compatibility policy, supported matrix, input schema guide, output/history semantics, and a clear distinction between `respondpy` and the underlying `respond` engine.

**Can wait until after v1**

- macOS wheels, if macOS is intentionally out of scope for v1.
- Formal schema migration tooling.
- Property-based testing across arbitrary state dimensions.
- Dependency provenance and artifact signing improvements.
- Additional convenience APIs around data creation and result export.

The highest-value v1 work is therefore: **freeze the API, align runtime/stubs/docs, define the support matrix, validate released artifacts, formalize the input schema, and add scientific correctness regressions.**

## Public API Freeze Checklist

Each area should answer:

- Is it public?
- What behavior is guaranteed?
- What inputs and outputs are accepted?
- What errors are raised?
- Is it documented and tested?
- Does runtime behavior match the stubs?

### 1. Top-Level Namespace

Review `src/respondpy/__init__.py` and `src/respondpy/data/__init__.py`.

- [ ] Freeze `respondpy.__all__` and `respondpy.__dir__()`.
- [ ] Decide whether `Input`, `HistoryMode`, and logging enums are top-level or module-only.
- [ ] Decide whether `_core` is public or implementation-only.
- [ ] Confirm all builder exports and names.

### 2. Input and Data API

Review `src/respondpy/data/input.py`, `parameters.py`, and the data helper modules.

- [ ] Freeze `Input` construction, required files, properties, and query methods.
- [ ] Document the SQLite schema and required configuration keys.
- [x] Validate required RESPOND tables and columns when constructing `Input`.
- [x] Document required simulation configuration keys and validate their basic values.
- [ ] Freeze `select_parameter()` shapes, dtypes, and `raw=True` behavior.
- [ ] Freeze parameter insert-row formats and state ordering.
- [ ] Freeze `ParameterType` members and their meanings.
- [ ] Define missing-row, duplicate-row, and invalid-value behavior.
- [x] Provide `Input.close()` and context-manager usage with deterministic post-close behavior.

### 3. Model and Simulation

Review the model and simulation stubs, `src/register_model.cpp`, and `src/register_simulation.cpp`.

- [ ] Freeze constructors, defaults, accepted state-vector shapes, and timestep indexing.
- [x] Accept state vectors with shapes `(m,)`, `(m, 1)`, and `(1, m)` and return one-dimensional vectors.
- [x] Support Python negative indices for model timesteps and timestep transitions.
- [x] Return independent model copies from simulation accessors and clone models on insertion/replacement.
- [ ] Define `run_timestep()`, `run_timesteps()`, and `Simulation.run()` semantics.
- [ ] Define model naming, indexing, insertion, replacement, cloning, and ownership.
- [ ] Define index bounds and negative-index behavior.
- [ ] Verify copy and deepcopy behavior.
- [ ] Freeze runtime configuration accessors.

### 4. Timesteps and Transitions

Review the timestep and transition stubs plus `src/register_timestep.cpp` and `src/register_transition.cpp`.

- [ ] Freeze constructors and supported transition names.
- [ ] Freeze transition ordering, matrix shapes, and dtypes.
- [ ] Define named versus indexed access and replacement behavior.
- [ ] Define matrix ownership and copy behavior.
- [ ] Define errors for unsupported transition types and invalid matrices.
- [ ] Confirm whether `Transition.execute()` mutates or returns new history data.
- [x] Remove duplicate native registrations before freezing the bindings.

### 5. Histories

Review the history stub and `src/register_history.cpp`.

- [ ] Freeze snapshot and accumulated history modes.
- [ ] Define sparse timestep, duplicate timestep, and pending-state behavior.
- [ ] Freeze `get_state_map()` and `get_state_as_vector()` semantics.
- [ ] Define vector dimensionality and zero-filling behavior.
- [ ] Freeze default history names and capture intervals.
- [ ] Define equality, copy, and representation behavior.
- [x] Resolve the `History.has_pending_state()` runtime/stub discrepancy.

### 6. Configuration and Logging

Review `config.py`, `logging.py`, their stubs, and native registration files.

- [ ] Freeze default execution and logging settings.
- [ ] Define thread-count and concurrent-model behavior.
- [ ] Define logger creation, reuse, collision, and shared-sink behavior.
- [ ] Define behavior when a logger does not exist.
- [ ] Freeze logger levels and public message functions.
- [ ] Document logging guarantees across threads and simulations.

### 7. Cost-Effectiveness Helpers

Review `cost_effectiveness.py`, its stub, and native registration.

- [ ] Freeze accepted array dimensionality, dtypes, and output types.
- [ ] Define length-mismatch behavior.
- [ ] Document discounting and timestep-zero semantics.
- [ ] Define `calculate_life_years()` assumptions and week-count behavior.
- [ ] Define numerical error behavior.

### 8. Builder API

Review `src/respondpy/build.py` and `docs/source/references/build.md`.

- [ ] Freeze all `build_*` functions and `add_matrix_to_transition()`.
- [ ] Freeze default transition order and parameter-change scheduling.
- [ ] Define processor-count and logger behavior.
- [ ] Define overdose, fatality, and mortality composition.
- [ ] Define missing-cohort and missing-time-row errors.

### 9. Typing and Runtime Parity

Review every file under `src/respondpy/_core`, the Python facades, and `tests/test_typing_stubs_mypy.py`.

- [ ] Confirm every public binding has a matching stub.
- [ ] Confirm every stub method exists at runtime.
- [ ] Confirm signatures, defaults, return shapes, and dtypes match.
- [ ] Confirm `__repr__`, equality, copy, deepcopy, and serialization coverage.
- [x] Remove the non-callable native `Model.serialize()` binding and stub.
- [x] Resolve the `History.has_pending_state()` discrepancy.
- [x] Reconcile `StateVector` annotations with accepted NumPy shapes.

### 10. Serialization, Ownership, and Threading

Review native headers, binding files, and lifecycle documentation.

- [x] Define `Model.to_json()` as the versioned JSON inspection format.
- [x] Document the `Model.to_json()` schema and explicit non-resumable limitations.
- [ ] Decide whether transition serialization is public.
- [x] Freeze copy-versus-reference behavior for accessors.
- [x] Define clone-on-insert and object lifetime behavior.
- [ ] Document thread-safety and concurrent `Simulation.run()` behavior.
- [ ] Document Eigen-thread restrictions and shared logging guarantees.

### 11. Tests and Documentation

- [ ] Test exact public exports.
- [ ] Test every public binding/stub pair.
- [ ] Add serialization and pending-history tests.
- [ ] Test copy/deepcopy contracts across runtime objects.
- [ ] Test named/indexed transition operations and ownership.
- [ ] Test canonical RESPONDv2 database compatibility.
- [ ] Make executable examples pass.
- [ ] Document the compatibility policy, input schema, output/history semantics, and `respondpy` versus `respond` responsibilities.

## Recommended Review Order

1. Top-level exports
2. Model and Simulation
3. Timestep and Transition
4. Histories
5. Input and data schema
6. Builders
7. Configuration and logging
8. Cost-effectiveness
9. Typing parity
10. Serialization and threading
11. Tests and documentation