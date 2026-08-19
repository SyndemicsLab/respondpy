################################################################################
# File: test_bench_end_to_end.py                                               #
# Project: respondpy                                                           #
# Created Date: 2026-05-06                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-16                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""
End-to-end benchmarks for the respondpy simulation pipeline.

Three phases are benchmarked individually and as a combined pipeline:
    1. load   — read data from SQLite and construct the Simulation
    2. run    — execute all model transitions for the full duration
    3. write  — export all model histories to CSV files

Run with:
    uv run pytest benchmarks/ -v --benchmark-only
Or via the nox session:
    uv run nox -s benchmark
"""

from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

from respondpy import Simulation, build_simulation
from respondpy.data import Input

# ---------------------------------------------------------------------------
# CSV history writer (local to benchmarks — not part of the distributed lib)
# ---------------------------------------------------------------------------


def _write_histories_to_csv(sim: Simulation, out_dir: Path) -> None:
    """Write each model's recorded state histories to a separate CSV file.

    Output format per file:
        history_name, timestep, state_0, state_1, ..., state_n

    Files are named ``<model_name>_histories.csv`` and written to *out_dir*.
    """
    for model_idx, model_name in enumerate(sim.get_model_names()):
        model_history = sim.get_model_history(model_idx)
        rows: list[dict] = []
        for hist_name, history in model_history.items():
            state_map = history.get_state_map()
            for timestep in history.get_recorded_timesteps():
                vec = state_map[timestep]
                row = {"history_name": hist_name, "timestep": int(timestep)}
                row.update({f"state_{i}": float(v) for i, v in enumerate(vec)})
                rows.append(row)
        if rows:
            pl.DataFrame(rows).write_csv(
                out_dir / f"{model_name}_histories.csv")


# ---------------------------------------------------------------------------
# Phase 1 — load
# ---------------------------------------------------------------------------

@pytest.mark.benchmark
def test_bench_load_data(benchmark, benchmark_db, benchmark_config):
    """Benchmark SQLite data loading and Simulation construction.

    Each round builds a fresh Input instance so the measurement captures the
    cold load path rather than reusing cached parameter arrays or sample ids.
    """

    def _build_from_scratch():
        input_data = Input(db_path=benchmark_db, conf_path=benchmark_config)
        return build_simulation(input_data, cohort_ids=[1])

    benchmark.pedantic(
        _build_from_scratch,
        rounds=10,
        iterations=1,
    )


# ---------------------------------------------------------------------------
# Phase 2 — run
# ---------------------------------------------------------------------------

@pytest.mark.benchmark
def test_bench_run_model(benchmark, benchmark_db, benchmark_config):
    """Benchmark sim.run() in isolation.

    The Simulation is rebuilt fresh before each round so that history state
    from a prior run does not carry over and inflate subsequent measurements.
    """
    def _setup():
        input_data = Input(db_path=benchmark_db, conf_path=benchmark_config)
        sim = build_simulation(input_data, cohort_ids=[1])
        return (sim,), {}

    benchmark.pedantic(
        lambda sim: sim.run(),
        setup=_setup,
        rounds=10,
        iterations=1,
    )


# ---------------------------------------------------------------------------
# Phase 3 — write
# ---------------------------------------------------------------------------

@pytest.mark.benchmark
def test_bench_write_histories(benchmark, benchmark_db, benchmark_config, tmp_path):
    """Benchmark CSV history export in isolation.

    The Simulation is built and run once in setup; only the CSV write is timed.
    """
    def _setup():
        input_data = Input(db_path=benchmark_db, conf_path=benchmark_config)
        sim = build_simulation(input_data, cohort_ids=[1])
        sim.run()
        return (sim, tmp_path), {}

    benchmark.pedantic(
        _write_histories_to_csv,
        setup=_setup,
        rounds=10,
        iterations=1,
    )


# ---------------------------------------------------------------------------
# Combined — end-to-end
# ---------------------------------------------------------------------------

@pytest.mark.benchmark
def test_bench_end_to_end(benchmark, benchmark_db, benchmark_config, tmp_path):
    """Benchmark the full pipeline: load → run → write CSV.

    Use this figure for direct comparison with RESPONDv1 wall-clock timings.
    """
    def _pipeline():
        input_data = Input(db_path=benchmark_db, conf_path=benchmark_config)
        sim = build_simulation(input_data, cohort_ids=[1])
        sim.run()
        _write_histories_to_csv(sim, tmp_path)

    benchmark.pedantic(
        _pipeline,
        rounds=10,
        iterations=1,
    )
