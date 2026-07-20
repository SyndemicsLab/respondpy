################################################################################
# File: test_smoke.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-20                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""
Smoke Tests to ensure RESPOND compiled. 
Run with `uv run pytest -m smoke`.
"""

from __future__ import annotations

import pytest
import numpy as np

import respondpy as rpy


@pytest.mark.smoke
def test_import() -> None:
    """Test that we can import the module."""
    import respondpy
    assert respondpy.__version__ is not None


@pytest.mark.smoke
def test_data_import() -> None:
    import respondpy.data
    assert respondpy.data.__all__ is not None
    assert isinstance(respondpy.__dir__(), list)


@pytest.mark.smoke
def test_model_Nx0() -> None:
    state = np.array([10.0, 20.0, 30.0]).squeeze()
    model = rpy.Model("markov")
    model.set_state(state)
    np.testing.assert_array_equal(state, model.get_state())


@pytest.mark.smoke
def test_model_1xN() -> None:
    state = np.array([[10.0, 20.0, 30.0]]).squeeze()
    model = rpy.Model("markov", "respond")
    print(state.shape)
    model.set_state(state)
    np.testing.assert_array_equal(state, model.get_state())


@pytest.mark.smoke
def test_model_Nx1() -> None:
    state = np.array([[10.0], [20.0], [30.0]])
    model = rpy.Model("markov", "respond", "respond.log")
    model.set_state(state)
    np.testing.assert_array_equal(state.squeeze(), model.get_state())


@pytest.mark.smoke
def test_one_step() -> None:
    state = np.array([1.3, 1.1, 1.8])
    migra = np.zeros((3, 1))

    model = rpy.Model("markov")
    model.set_state(state)

    timestep = rpy.Timestep("console")

    migr = timestep.create_transition("migration")
    migr.add_transition_matrix(migra)
    model.add_timestep(timestep)
    model.run_timesteps()

    np.testing.assert_equal(model.get_state().shape, (3,))


@pytest.mark.smoke
def test_simulation_sparse_histories() -> None:
    """Verify simulation exposes model histories as name-keyed dict of History objects."""
    state = np.array([10.0, 20.0, 30.0])
    model = rpy.Model("markov")
    model.set_state(state)
    model.create_default_histories()

    sim = rpy.Simulation()
    sim.add_model(model)
    sim.run()

    model_histories = sim.get_model_history("markov")
    assert isinstance(
        model_histories, dict), "Expected dict keyed by history name"

    for hist in model_histories.values():
        assert isinstance(
            hist, rpy.History), "Expected History values in dict"
