################################################################################
# File: test_smoke_bindings_runtime.py                                         #
# Project: respondpy                                                           #
# Created Date: 2026-07-22                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-22                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""Smoke tests validating pybind runtime contracts for core bindings."""

from __future__ import annotations

import numpy as np
import pytest

import respondpy as rpy
from respondpy.history import HistoryMode


@pytest.mark.smoke
def test_transition_execute_returns_state_and_history_tuple() -> None:
    """Transition.execute should return both the updated state and history map."""
    transition = rpy.Transition("migration")
    transition.add_matrix(np.zeros((3, 1)))
    input_state = np.array([1.0, 2.0, 3.0])

    result = transition.execute(input_state, {})

    assert isinstance(result, tuple), (
        "Expected Transition.execute to return a tuple of "
        "(StateVector, history_map)."
    )
    assert len(result) == 2, (
        "Expected Transition.execute tuple to have exactly 2 elements: "
        "state and history map."
    )

    output_state, output_history = result
    np.testing.assert_equal(
        output_state.shape,
        input_state.shape,
        err_msg="Expected output state shape to match input state shape.",
    )
    assert isinstance(output_history, dict), (
        "Expected Transition.execute second return value to be a dict-like "
        "history mapping."
    )


@pytest.mark.smoke
def test_history_mode_members_and_latest_timestep_method_are_exposed() -> None:
    """History bindings should expose enum members and latest timestep accessor."""
    assert hasattr(HistoryMode, "kSnapshot"), (
        "Expected HistoryMode to expose enum member 'kSnapshot'."
    )
    assert hasattr(HistoryMode, "kAccumulated"), (
        "Expected HistoryMode to expose enum member 'kAccumulated'."
    )

    history = rpy.History("state")
    assert hasattr(history, "get_latest_recorded_timestep"), (
        "Expected History to expose method 'get_latest_recorded_timestep'."
    )


@pytest.mark.smoke
def test_simulation_create_new_model_returns_model_and_registers_model() -> None:
    """Simulation.create_new_model should return a cloned Model instance."""
    simulation = rpy.Simulation()
    created_model = simulation.create_new_model("markov")

    assert isinstance(created_model, rpy.Model), (
        "Expected Simulation.create_new_model to return a Model instance."
    )
    assert created_model.get_name() == "markov", (
        "Expected returned model to use the requested model type name."
    )
    assert simulation.get_model_names() == ["markov"], (
        "Expected simulation to register one canonical model name: 'markov'."
    )
    assert isinstance(simulation.get_model(0), rpy.Model), (
        "Expected get_model(0) to return a Model instance after creation."
    )


@pytest.mark.smoke
def test_simulation_get_model_returns_live_mutable_model_reference() -> None:
    """Mutating a model from get_model should update the simulation-owned model."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    expected_state = np.array([3.0, 2.0, 1.0])
    model = simulation.get_model(0)
    model.set_state(expected_state)

    np.testing.assert_array_equal(
        simulation.get_model(0).get_state(),
        expected_state,
        err_msg="Expected get_model to expose a live simulation-owned model.",
    )


@pytest.mark.smoke
def test_simulation_set_model_replaces_model_by_index() -> None:
    """set_model(index, model) should replace the stored model state."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    replacement = rpy.Model("markov")
    replacement_state = np.array([7.0, 8.0, 9.0])
    replacement.set_state(replacement_state)

    simulation.set_model(0, replacement)

    np.testing.assert_array_equal(
        simulation.get_model(0).get_state(),
        replacement_state,
        err_msg="Expected set_model to replace the simulation model at index.",
    )


@pytest.mark.smoke
def test_simulation_index_setitem_replaces_model_by_index() -> None:
    """Simulation[index] assignment should replace the stored model."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    replacement = rpy.Model("markov")
    replacement_state = np.array([4.0, 5.0, 6.0])
    replacement.set_state(replacement_state)

    simulation[0] = replacement

    np.testing.assert_array_equal(
        simulation[0].get_state(),
        replacement_state,
        err_msg="Expected __setitem__ to replace the simulation model at index.",
    )


@pytest.mark.smoke
def test_binding_failure_messages_follow_expected_patterns() -> None:
    """Binding exceptions should surface informative message patterns."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    with pytest.raises(Exception, match=r"(?i)(out of bounds|index)"):
        simulation.get_model(999)

    timestep = rpy.Timestep()
    with pytest.raises(Exception, match=r"(?i)(not found|transition)"):
        timestep.get_transition("missing")

    with pytest.raises(TypeError, match=r"(?i)incompatible constructor arguments"):
        _ = rpy.Simulation(1)  # type: ignore[arg-type]
