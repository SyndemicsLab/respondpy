################################################################################
# File: test_smoke.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-05                                                    #
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
def test_model() -> None:
    state = np.array([10, 20, 30])
    model = rpy.Model("markov", "console")
    model.set_state(state)
    np.testing.assert_array_equal(state, model.get_state())


@pytest.mark.smoke
def test_one_step() -> None:
    state = np.array([[1.3], [1.1], [1.8]])
    migra = np.array([[0.0], [0.0], [0.0]])
    inter = np.array([[0.1, 0.2, 0.5], [0.3, 0.2, 0.3], [0.7, 0.2, 0.3]])
    behav = np.array([[0.3, 0.2, 0.1], [0.4, 0.2, 0.1], [0.3, 0.4, 0.1]])
    overd = np.array([[0.01], [0.01], [0.02]])
    fatal = np.array([[0.01], [0.01], [0.01]])
    backg = np.array([[0.001], [0.001], [0.002]])

    model = rpy.Model("markov", "console")
    model.set_state(state)

    migr = rpy.Transition("migration", "console")
    migr.add_transition_matrix(migra)
    model.add_transition(migr)

    beha = rpy.Transition("behavior", "console")
    beha.add_transition_matrix(behav)
    model.add_transition(beha)

    inte = rpy.Transition("intervention", "console")
    inte.add_transition_matrix(inter)
    model.add_transition(inte)

    over = rpy.Transition("overdose", "console")
    over.add_transition_matrix(overd)
    over.add_transition_matrix(fatal)
    model.add_transition(over)

    back = rpy.Transition("background_death", "console")
    back.add_transition_matrix(backg)
    model.add_transition(back)

    model.run_transitions()

    assert model.get_transition_names(
    ) == ["migration", "behavior", "intervention", "overdose", "background_death"]
    print(model.get_state())
    expected = [0.76715528791564891, 0.72320370216816077, 1.037712429738102]
    np.testing.assert_almost_equal(model.get_state(), expected)


@pytest.mark.smoke
def test_simulation_sparse_histories() -> None:
    """Verify get_model_sparse_histories returns a name-keyed dict of History objects."""
    state = np.array([10.0, 20.0, 30.0])
    model = rpy.Model("markov", "console")
    model.set_state(state)
    model.create_default_histories()

    sim = rpy.Simulation()
    sim.add_model(model)
    sim.run()

    sparse = sim.get_model_sparse_histories()

    assert isinstance(sparse, dict), "Expected a dict keyed by model name"
    assert "markov" in sparse, "Expected 'markov' model name as key"

    model_histories = sparse["markov"]
    assert isinstance(
        model_histories, dict), "Expected inner dict keyed by history name"

    for hist in model_histories.values():
        assert isinstance(
            hist, rpy.History), "Expected History values in inner dict"
