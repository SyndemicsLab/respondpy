################################################################################
# File: test_typing_stubs_mypy.py                                              #
# Project: respondpy                                                           #
# Created Date: 2026-07-22                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-09-25                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""Smoke tests that validate stub behavior via mypy through uv."""

from __future__ import annotations

from pathlib import Path
import subprocess

import pytest


def _run_mypy(path: Path) -> subprocess.CompletedProcess[str]:
    """Run mypy through uv for a single smoke snippet file."""
    repo_root = Path(__file__).resolve().parent.parent
    return subprocess.run(
        [
            "uv",
            "run",
            "mypy",
            "--no-color-output",
            "--hide-error-context",
            str(path),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.typing
def test_mypy_typing_positive_stub_usage(tmp_path: Path) -> None:
    """Typed usage matching stubs should pass mypy."""
    test_file = tmp_path / "stub_smoke_positive.py"
    test_file.write_text(
        """from __future__ import annotations

import numpy as np
import respondpy as rpy
from respondpy.history import HistoryMode

runtime_config = rpy.RuntimeConfig()
runtime_config.execution.total_threads = 2
logging_status: rpy.logging.CreationStatus = rpy.logging.configure_logger(
    runtime_config.logging
)
logger_info: str = rpy.logging.get_logger_info(runtime_config.logging.logger_name)
rpy.logging.set_log_pattern(rpy.logging.LogPattern.kStandard)
rpy.logging.set_logger_level(runtime_config.logging.logger_name, 2)
model_with_config: rpy.Model = rpy.Model("markov", runtime_config)
simulation_with_config = rpy.Simulation(runtime_config)
simulation_with_config.set_execution_config(runtime_config.execution)
execution_config: rpy.ExecutionConfig = simulation_with_config.get_execution_config()
 
state = np.array([1.0, 2.0, 3.0], dtype=float)
transition = rpy.Transition("migration")
transition.add_matrix(np.zeros((3, 1)))
next_state, history_map = transition.execute(state, {})

created_model: rpy.Model = rpy.Simulation().create_new_model("markov")
mode: HistoryMode = HistoryMode.kSnapshot
latest_timestep: int = int(rpy.History("state").get_latest_recorded_timestep())

assert isinstance(created_model, rpy.Model)
assert isinstance(model_with_config, rpy.Model)
assert isinstance(execution_config.total_threads, int)
assert isinstance(logging_status, rpy.logging.CreationStatus)
assert isinstance(logger_info, str)
assert latest_timestep >= -1
assert next_state.shape == state.shape
assert isinstance(history_map, dict)
assert mode.name == "kSnapshot"
""",
        encoding="utf-8",
    )

    result = _run_mypy(test_file)
    assert result.returncode == 0, (
        "Expected mypy smoke positive snippet to pass.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@pytest.mark.typing
def test_mypy_typing_negative_stub_misuse(tmp_path: Path) -> None:
    """Typed misuse should fail mypy with informative message patterns."""
    test_file = tmp_path / "stub_smoke_negative.py"
    test_file.write_text(
        """from __future__ import annotations

import numpy as np
import respondpy as rpy

bad_model: int = rpy.Simulation().create_new_model("markov")
state = np.array([1.0, 2.0, 3.0], dtype=float)
transition = rpy.Transition("migration")
transition.add_matrix(np.zeros((3, 1)))
_ = transition.execute(state, 123)
_ = rpy.History("state").get_latest_recorded_timestep("oops")
""",
        encoding="utf-8",
    )

    result = _run_mypy(test_file)
    combined = f"{result.stdout}\n{result.stderr}"

    assert result.returncode != 0, (
        "Expected mypy smoke negative snippet to fail, but it passed.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "Incompatible types in assignment" in combined, (
        "Expected mypy to report assignment type mismatch for create_new_model."
    )
    assert "execute" in combined and "incompatible type" in combined.lower(), (
        "Expected mypy to report incompatible type for Transition.execute history argument."
    )
    assert "Too many arguments" in combined and "get_latest_recorded_timestep" in combined, (
        "Expected mypy to report incorrect argument count for latest timestep accessor."
    )
