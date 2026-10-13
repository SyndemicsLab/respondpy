################################################################################
# File: test_index_normalization.py                                            #
# Project: respondpy                                                           #
# Created Date: 2026-10-13                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-10-13                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""Focused tests for Python-style index normalization in bindings."""

import pytest

import respondpy as rpy


@pytest.mark.unit
def test_simulation_model_indexes_support_negative_and_reject_bounds() -> None:
    simulation = rpy.Simulation()
    simulation.create_new_model("first")
    simulation.create_new_model("second")

    assert simulation.get_model(0).get_name() == "first"
    assert simulation.get_model(-1).get_name() == "second"

    with pytest.raises(IndexError, match="index out of range"):
        simulation.get_model(2)
    with pytest.raises(IndexError, match="index out of range"):
        simulation.get_model(-3)


@pytest.mark.unit
def test_timestep_transition_indexes_support_negative_and_reject_bounds() -> (
    None
):
    timestep = rpy.Timestep()
    timestep.create_transition("migration")
    timestep.create_transition("behavior")

    assert timestep.get_transition(0).get_name() == "migration"
    assert timestep.get_transition(-1).get_name() == "behavior"

    with pytest.raises(IndexError, match="index out of range"):
        timestep.get_transition(2)
    with pytest.raises(IndexError, match="index out of range"):
        timestep.get_transition(-3)


@pytest.mark.unit
def test_model_timestep_indexes_support_negative_and_reject_bounds() -> None:
    model = rpy.Model("markov", rpy.RuntimeConfig())
    first = rpy.Timestep()
    first.create_transition("migration")
    second = rpy.Timestep()
    second.create_transition("behavior")
    model.add_timestep(first)
    model.add_timestep(second)

    assert model.get_timestep_at_index(0).get_transition_names() == [
        "migration"
    ]
    assert model.get_timestep_at_index(-1).get_transition_names() == [
        "behavior"
    ]

    with pytest.raises(IndexError, match="index out of range"):
        model.get_timestep_at_index(2)
    with pytest.raises(IndexError, match="index out of range"):
        model.get_timestep_at_index(-3)
