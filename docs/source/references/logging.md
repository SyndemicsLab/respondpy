# Reference: Logging

API reference for RESPOND logging functions exposed to Python.

This module forwards directly to the C++ RESPOND logging backend, so Python and
C++ can write to the same logger and output file.

## Shared-sink workflow

For concurrent models or threads that write to one file, create the shared
sink before creating the logger, then configure runtime objects to use that
logger:

```python
import respondpy as rpy

rpy.logging.create_shared_file_sink("respond.log")
rpy.logging.create_shared_logger("respond")

config = rpy.RuntimeConfig()
config.logging.logger_name = "respond"
config.logging.file_path = "respond.log"
config.logging.use_shared_sink = True
simulation = rpy.Simulation(config)
```

`create_shared_file_sink()` and `create_shared_logger()` return a
`CreationStatus`. Reusing an existing destination is supported; callers can
use `check_logger_exists()` and `flush_all_loggers()` when coordinating
multiple writers.

See also:
- [How-To: Select Cohorts and Configure Logging](../how_to/cohort_subset_and_logging.md)
- [Reference: respondpy Package](package.md)

```{automodule} respondpy.logging
:members:
:undoc-members:
:show-inheritance:
```
