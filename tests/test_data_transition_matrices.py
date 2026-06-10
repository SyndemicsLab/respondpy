################################################################################
# File: test_data_transition_matrices.py                                       #
# Project: respondpy                                                           #
# Created Date: 2026-06-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-10                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import pytest
import polars as pl

import respondpy.data as rpydata


@pytest.mark.unit
def test_build_constant_transition_intervention() -> None:
    inter = [f"I{i}" for i in range(16)]
    behav = [f"B{j}" for j in range(4)]
    df = rpydata.build_constant_transition(inter, behav).collect()
    assert df.shape == ((16 * 4)**2, 7)
    assert set(df.columns) == {
        "sample", "time", "initial_intervention", "new_intervention", "initial_behavior", "new_behavior", "probability"}


@pytest.mark.unit
def test_update_retention_probability_valid_one() -> None:
    df = pl.DataFrame({
        "sample": [1, 1, 1, 1],
        "time": [0, 0, 0, 0],
        "initial_intervention": ["A", "A", "B", "B"],
        "new_intervention": ["A", "B", "A", "B"],
        "initial_behavior": ["X", "X", "X", "X"],
        "new_behavior": ["X", "X", "X", "X"],
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
        "initial_intervention": ["A", "A", "A", "A"],
        "new_intervention": ["A", "A", "A", "A"],
        "initial_behavior": ["X", "X", "Y", "Y"],
        "new_behavior": ["X", "Y", "X", "Y"],
        "probability": [0.6, 0.2, 1.0, 0.0]
    })

    updated_df = rpydata.update_retention_probability(
        df, "initial_intervention", "new_intervention")

    expected_probabilities = [0.8, 0.2, 1.0, 0.0]
    assert updated_df["probability"].to_list() == expected_probabilities


@pytest.mark.unit
def test_update_retention_probability_valid_three() -> None:
    df = pl.DataFrame({
        "sample": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "time": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "initial_intervention": [
            "A", "A", "A", "A", "A", "A", "A", "A",
            "B", "B", "B", "B", "B", "B", "B", "B"
        ],
        "new_intervention": [
            "A", "A", "A", "A", "B", "B", "B", "B",
            "A", "A", "A", "A", "B", "B", "B", "B"
        ],
        "initial_behavior": [
            "X", "X", "Y", "Y", "X", "X", "Y", "Y",
            "X", "X", "Y", "Y", "X", "X", "Y", "Y"
        ],
        "new_behavior": [
            "X", "Y", "X", "Y", "X", "Y", "X", "Y",
            "X", "Y", "X", "Y", "X", "Y", "X", "Y"
        ],
        "probability": [
            0.6, 0.0, 0.0, 0.4, 0.3, 0.0, 0.0, 0.5,
            0.6, 0.0, 0.0, 0.2, 0.6, 0.0, 0.0, 1.0
        ]
        # rx, z, z, ry, tx, z, z, ty
        # tx, z, z, ty, rx, z, z, ry
    })
    from_cols = ["initial_intervention", "initial_behavior"]
    to_cols = ["new_intervention", "new_behavior"]
    updated_df = rpydata.update_retention_probability(df, from_cols, to_cols)

    expected_probabilities = [0.7, 0.0, 0.0, 0.5, 0.3, 0.0, 0.0, 0.5,
                              0.6, 0.0, 0.0, 0.2, 0.4, 0.0, 0.0, 0.8]
    assert updated_df["probability"].to_list() == expected_probabilities


@pytest.mark.unit
def test_update_retention_probability_valid_four() -> None:
    df = pl.DataFrame({
        "sample": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "time": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "initial_intervention": [
            "A", "A", "A", "A", "A", "A", "A", "A",
            "B", "B", "B", "B", "B", "B", "B", "B"
        ],
        "new_intervention": [
            "A", "A", "A", "A", "B", "B", "B", "B",
            "A", "A", "A", "A", "B", "B", "B", "B"
        ],
        "initial_behavior": [
            "X", "X", "Y", "Y", "X", "X", "Y", "Y",
            "X", "X", "Y", "Y", "X", "X", "Y", "Y"
        ],
        "new_behavior": [
            "X", "Y", "X", "Y", "X", "Y", "X", "Y",
            "X", "Y", "X", "Y", "X", "Y", "X", "Y"
        ],
        "probability": [
            0.6, 0.3, 0.2, 0.4, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.1, 1.0
        ]
        # rx, tx, ty, ry, z, z, z, z
        # z, z, z, z, rx, tx, ty, ry
    })

    updated_df = rpydata.update_retention_probability(
        df, "initial_intervention", "new_intervention")

    expected_probabilities = [0.7, 0.3, 0.2, 0.8, 0.0, 0.0, 0.0, 0.0,
                              0.0, 0.0, 0.0, 0.0, 0.8, 0.2, 0.1, 0.9]
    assert updated_df["probability"].to_list() == expected_probabilities
