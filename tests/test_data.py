################################################################################
# File: test_data.py                                                           #
# Project: respondpy                                                           #
# Created Date: 2026-06-02                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-02                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl
import pytest

from respondpy import (
    update_retention_probability,
    verify_transition_probability,
)


@pytest.mark.unit
def test_verify_transition_probability_happy_path() -> None:
    transition_matrix = pl.DataFrame(
        {
            "sample": [1, 1, 1, 1],
            "time": [1, 1, 1, 1],
            "initial_intervention": [1, 1, 2, 2],
            "behavior": [1, 1, 1, 1],
            "new_intervention": [1, 2, 1, 2],
            "probability": [0.8, 0.2, 0.4, 0.6],
        }
    )

    assert verify_transition_probability(
        transition_matrix,
        "initial_intervention",
        probability_column="probability",
    )


@pytest.mark.unit
def test_update_retention_probability_happy_path() -> None:
    # Matrix is intentionally incomplete and missing retention rows.
    partial = pl.DataFrame(
        {
            "sample": [1, 1],
            "time": [1, 1],
            "initial_intervention": [1, 2],
            "behavior": [1, 1],
            "new_intervention": [2, 1],
            "probability": [0.2, 0.4],
        }
    )

    result = update_retention_probability(
        partial,
        "initial_intervention",
        "new_intervention",
        probability_column="probability",
    ).sort(["sample", "time", "initial_intervention", "behavior", "new_intervention"])

    expected = pl.DataFrame(
        {
            "sample": [1, 1, 1, 1],
            "time": [1, 1, 1, 1],
            "initial_intervention": [1, 1, 2, 2],
            "behavior": [1, 1, 1, 1],
            "new_intervention": [1, 2, 1, 2],
            "probability": [0.8, 0.2, 0.4, 0.6],
        }
    )

    assert result.equals(expected)
    assert verify_transition_probability(result, "initial_intervention")


@pytest.mark.unit
def test_update_retention_probability_expanded_matrix_happy_path() -> None:
    expanded = pl.DataFrame(
        {
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 1, 1, 1],
            "next_intervention": [1, 2, 1, 2],
            "next_behavior": [1, 1, 1, 1],
            "probability": [0.0, 0.2, 0.4, 0.0],
        }
    )

    result = update_retention_probability(
        expanded,
        "intervention",
        "next_intervention",
        probability_column="probability",
        group_columns=["intervention", "behavior"],
        unique_key_columns=[
            "intervention",
            "behavior",
            "next_intervention",
            "next_behavior",
        ],
        retention_pairs=[
            ("intervention", "next_intervention"),
            ("behavior", "next_behavior"),
        ],
        complete_missing=False,
    ).sort(["intervention", "behavior", "next_intervention", "next_behavior"])

    expected = pl.DataFrame(
        {
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 1, 1, 1],
            "next_intervention": [1, 2, 1, 2],
            "next_behavior": [1, 1, 1, 1],
            "probability": [0.8, 0.2, 0.4, 0.6],
        }
    )

    assert result.equals(expected)
    assert verify_transition_probability(
        result,
        "intervention",
        group_columns=["intervention", "behavior"],
        unique_key_columns=[
            "intervention",
            "behavior",
            "next_intervention",
            "next_behavior",
        ],
    )
