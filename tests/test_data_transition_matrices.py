################################################################################
# File: test_data_transition_matrices.py                                       #
# Project: respondpy                                                           #
# Created Date: 2026-06-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import pytest
import polars as pl

import respondpy.data as rpydata


@pytest.mark.unit
def test_build_constant_transition_intervention() -> None:
    parameter = rpydata.Parameter(
        rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY)

    df = rpydata.build_constant_transition(parameter, 16, 4)
    assert df.shape == (16 * 4 * 16, 6)
    assert set(df.columns) == {
        "sample", "time", "initial_intervention", "new_intervention", "behavior", "probability"}


@pytest.mark.unit
def test_build_constant_transition_behavior() -> None:
    parameter = rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY)

    df = rpydata.build_constant_transition(parameter, 16, 4)
    assert df.shape == (16 * 4 * 4, 6)
    assert set(df.columns) == {
        "sample", "time", "initial_behavior", "new_behavior", "intervention", "probability"}


@pytest.mark.unit
def test_build_constant_transition_invalid_parameter() -> None:
    parameter = rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    )

    with pytest.raises(ValueError, match="not a valid state transition"):
        rpydata.build_constant_transition(parameter, 16, 4)


@pytest.mark.unit
def test_update_retention_probability_valid_one() -> None:
    df = pl.DataFrame({
        "sample": [1, 1, 1, 1],
        "time": [0, 0, 0, 0],
        "initial_intervention": ["A", "A", "B", "B"],
        "new_intervention": ["A", "B", "A", "B"],
        "behavior": ["X", "X", "X", "X"],
        "probability": [0.0, 0.2, 1.0, 0.0]
    })

    updated_df = rpydata.update_retention_probability(
        df, "initial_intervention", "new_intervention")

    expected_probabilities = [0.8, 0.2, 1.0, 0.0]
    assert updated_df["probability"].to_list() == expected_probabilities


@pytest.mark.unit
def test_update_retention_probability_valid_two() -> None:
    df = pl.DataFrame({
        "sample": [1, 1, 1, 1],
        "time": [0, 0, 0, 0],
        "initial_intervention": ["A", "A", "B", "B"],
        "new_intervention": ["A", "B", "A", "B"],
        "behavior": ["X", "X", "X", "X"],
        "probability": [0.6, 0.2, 1.0, 0.0]
    })

    updated_df = rpydata.update_retention_probability(
        df, "initial_intervention", "new_intervention")

    expected_probabilities = [0.8, 0.2, 1.0, 0.0]
    assert updated_df["probability"].to_list() == expected_probabilities
