# RESPOND logging hotfix binding work

This document tracks the respondpy updates required for the `respond` repository
branch `hotfix/logging-issues` at commit `d5bb07a1d9bfecfc192db8a5610f1ed1672bcb8a`.
The previous comparison point is `v2.5.2` at commit
`738f5b5534b0c87a9b02d2c62c03f4b86ff9bd5f`.

The CMake dependency is already pinned to the hotfix in
`CMakeLists.txt`. The items below cover binding parity, behavior, typing,
testing, and packaging. Check them off in order as implementation proceeds.

## 1. Baseline and build

- [x] Record the current test and build baseline before changing bindings.
      `uv run pytest -m 'smoke or unit or integration'`: 146 passed, 4
      deselected.
- [x] Confirm the pinned upstream commit is available from the `respond`
      repository and is the revision used by the build directory.
- [x] Build the extension with the hotfix enabled through the isolated wheel
      build. `uv build --wheel` produced
      `respondpy-0.3.3-cp312-cp312-linux_x86_64.whl`.
- [x] Confirm `Threads::Threads` and the newly exported public headers do not
      require additional respondpy CMake changes. After selecting pybind11
      3.0.4, the native extension builds and links successfully.
- [x] Check wheel and install builds, not only the local developer build. The
      wheel build and CMake `install` target both pass.
- [x] Verify respondpy does not set removed upstream options such as
      `RESPOND_NO_EXCEPTIONS`. The obsolete `RESPOND_NO_EXCEPTIONS` and
      `RESPOND_RUN_OMP` entries were removed from `CMakePresets.json` during
      the successful hotfix configuration.

### Baseline findings

- The fetched dependency is `respond` commit `d5bb07a1d9bfecfc192db8a5610f1ed1672bcb8a`
  (`v2.5.2-11-gd5bb07a`).
- The isolated wheel build resolves pybind11 3.0.4 and succeeds.
- The repository CMake preset now resolves pybind11 3.0.4 after removing the
      system-package fallback from `FetchContent_Declare`; the native extension,
      install target, and binding smoke tests all pass.
- The preset no longer passes the obsolete `RESPOND_NO_EXCEPTIONS` or
      `RESPOND_RUN_OMP` options to the hotfix.
- The fetched upstream source has an unrelated working-tree modification in
  `build/_deps/respond-src/docs/src/math.md`; it was not changed here.

## 2. Runtime configuration bindings

The hotfix adds `ExecutionConfig`, `LoggingConfig`, and `RuntimeConfig`.

- [x] Add pybind classes for `ExecutionConfig`, including
      `total_threads`, `eigen_threads`, and `run_models_concurrently`.
- [x] Add pybind classes for `LoggingConfig`, including `logger_name`,
      `file_path`, and `use_shared_sink`.
- [x] Add pybind class for `RuntimeConfig`, containing execution and logging
      configuration.
- [x] Place the classes in the `_core.config` submodule and expose them through
      `respondpy.config` and the top-level package namespace.
- [x] Export the classes from `respondpy` where the public API expects them.
- [x] Add matching `.pyi` declarations and constructor defaults.
- [x] Test constructing, reading, and mutating each configuration object.

### Runtime configuration findings

- The native binding compiles and links against the pinned `respond` hotfix.
- The rebuilt package exposes `respondpy._core.config` and the three public
  classes.
- Configuration smoke tests pass: 10 passed.
- Typing stub tests pass: 2 passed.

## 3. Model and simulation APIs

- [x] Bind `Model::Create(name, RuntimeConfig)`.
- [x] Verify the existing model creation overloads remain usable while they
      are deprecated upstream.
- [x] Bind `Simulation(RuntimeConfig)`.
- [x] Verify the existing simulation constructors remain usable, including the
      hotfix's deprecated logger/execution-config constructor.
- [x] Bind `Simulation.get_execution_config()` and
      `Simulation.set_execution_config()`.
- [x] Bind `Simulation.get_runtime_config()` and
      `Simulation.set_runtime_config()`.
- [x] Update the `.pyi` signatures for all new overloads and accessors; the
      existing Python wrappers only re-export the bound classes and require no
      runtime logic changes.
- [x] Test configuration changes before and after a simulation is run.

### Model and simulation findings

- The native bindings compile and link with the new overloads.
- Runtime smoke tests pass: 12 passed, including model construction,
  simulation configuration accessors, a post-run configuration check, and the
  legacy three-argument simulation constructor.
- Typing stub tests pass: 2 passed, including the new constructors and
  execution-config accessor.

## 4. Logging API parity

Review the declarations in `respond/include/respond/logging.hpp` and expose
all new public operations needed by Python. In particular:

- [x] Bind `ConfigureLogger` from `LoggingConfig`.
- [x] Bind shared file sink creation and shared logger creation.
- [x] Bind logger existence/status queries.
- [x] Bind logger information and logger-level controls.
- [x] Bind global logger flushing and flush-interval controls.
- [x] Confirm `CreationStatus`, `LogType`, and `LogPattern` enum values and
      names match the Python stubs.
- [x] Update `respondpy.logging` wrappers and public exports.
- [x] Add matching `.pyi` declarations, argument names, and return types.
- [x] Test same-destination logger reuse, conflicting destinations, shared
      sinks, missing loggers, and repeated flushes.
- [x] Test concurrent logger creation and writes for duplicate sinks and
      incorrect status values.

### Logging API findings

- The native binding already exposed the shared-sink, query, level, pattern,
      flush, and message functions; `ConfigureLogger(LoggingConfig)` was the
      missing native operation.
- The Python facade now exports `configure_logger`, and the logging stubs match
      the hotfix argument names and return types.
- Logging parity smoke coverage passes: 13 selected logging/binding tests pass
      in the full smoke run, including concurrent shared-sink creation/writes.
- Typing stub tests pass: 2 passed.

## 5. Runtime behavior changes

The hotfix changes behavior even where the Python signature is unchanged.

- [x] Test that concurrent model execution rejects
      `eigen_threads > 1`.
- [x] Test valid concurrent execution with `eigen_threads <= 1`.
- [x] Test stricter simulation duration validation, including zero and other
      invalid negative values.
- [x] Test deferred timestep and transition-matrix validation at runtime.
- [x] Verify missing logger handling and resulting Python exceptions/messages.
- [x] Verify Eigen thread coordination when multiple simulations run.
- [x] Check history insertion ordering and copy/move behavior through returned
      Python objects.
- [x] Check cost-effectiveness discount results against the updated upstream
      behavior.

### Runtime behavior findings

- Concurrent execution rejects `eigen_threads > 1` and succeeds with
      `eigen_threads <= 1`; concurrent runs of multiple simulations also pass.
- `Simulation.run(0)`, `Simulation.run(< -1)`, and
      `Simulation.set_duration(<= 0)` raise the upstream validation messages.
- Transition matrices are accepted when added and rejected with a matrix-size
      error when execution later validates them.
- Missing logger queries report the logger as absent, while log messages are
      sent to stderr and are not persisted.
- History insertion remains ordered and copied histories are independent.
- Cost-effectiveness vector bindings now accept one-dimensional NumPy arrays,
      expose the documented default arguments, and match the hotfix discount
      calculation.

## 6. Tests and typing

- [x] Extend the smoke binding tests with configuration and logging workflows.
- [x] Extend model tests for the new and deprecated creation paths.
- [x] Extend simulation tests for constructors, accessors, validation, and
      concurrent execution.
- [x] Add or update logging tests for shared sinks and logger status handling.
- [x] Update typing tests for configuration classes, overloads, methods, and
      enums.
- [x] Run the focused tests first, then the complete test suite with warnings
      treated as errors.
- [x] Run static analysis and confirm no new binding or stub diagnostics.

### Tests and typing findings

- Focused runtime behavior tests pass: 3 passed.
- Full test suite passes with warnings treated as errors: 157 passed.
- Typing smoke tests pass: 2 passed.
- Pylint passes: 10.00/10.
- Strict mypy reports 20 pre-existing diagnostics confined to five
      `respondpy.data` modules; the updated binding and core stub diagnostics
      are clean. Core deepcopy stubs were parameterized and legacy model
      constructor typing was restored.

## 7. Documentation and release checks

- [x] Document the runtime configuration API and its defaults.
- [x] Document that concurrent model execution requires
      `eigen_threads <= 1`.
- [x] Document the shared-sink logging workflow.
- [x] Update logging, runtime-object, and wrapper-typing references as needed.
- [x] Confirm public exports, package metadata, and generated wheels contain
      the new API.
- [x] Record the minimum respond version or exact commit required by this
      release.

### Documentation and release findings

- Runtime configuration defaults and the concurrent execution constraint are
      documented in the runtime-object reference.
- Shared file-sink setup, status handling, and flushing are documented in the
      logging reference and existing logging how-to.
- Top-level exports and wrapper typing coverage are documented in the package
      and wrapper-typing references.
- The required upstream RESPOND revision is pinned and documented as
      `d5bb07a1d9bfecfc192db8a5610f1ed1672bcb8a`.
- `respondpy` version `0.3.3` metadata and generated wheel contents were
      checked during the release validation.

## Files expected to change

- `src/module.cpp`
- `src/register_logging.cpp`
- `src/register_model.cpp`
- `src/register_simulation.cpp`
- A new runtime-configuration registration source, if that matches the local
  binding organization
- `src/respondpy/__init__.py`
- `src/respondpy/logging.py`
- `src/respondpy/model.py`
- `src/respondpy/simulation.py`
- `src/respondpy/_core/*.pyi`
- Focused tests under `tests/`
- Relevant documentation under `docs/source/`

## Sign-off

- [x] All binding symbols have runtime and stub parity.
- [x] Existing public construction paths still work or have an intentional
      migration note.
- [x] Focused and full test suites pass.
- [x] Build, wheel, and installation checks pass.
- [x] Documentation matches the implemented public API.
