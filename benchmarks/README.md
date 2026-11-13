# respondpy Benchmarks

These opt-in benchmarks require a local RESPOND data directory containing
`input.db` and `sim.conf`. The supplied database and config are used directly;
benchmark data is not generated. All cohorts in `input.db` are included.

Run the benchmarks from the repository root:

```bash
uv run pytest benchmarks/ --benchmark-only -v \
  --benchmark-data-root /path/to/local/data \
  --benchmark-json /tmp/respondpy-benchmark.json
```

The measured round count is configured in `benchmark_config.toml` and can be
overridden with `--benchmark-rounds`. The same options can be passed through
the opt-in Nox session:

```bash
uv run nox -s benchmark -- \
  --benchmark-data-root /path/to/local/data \
  --benchmark-json /tmp/respondpy-benchmark.json
```

The build benchmark measures `build_simulation()` with `Input` initialized
before timing. The run benchmark measures `sim.run()` with a fresh simulation
per round. The write benchmark measures CSV history export after setup builds
and runs the simulation. The end-to-end benchmark includes input initialization,
simulation construction, execution, and CSV export.

Benchmarks are not part of CI. Keep timing comparisons tied to the same input
database, config, and machine; benchmark results are observational and do not
set test thresholds.