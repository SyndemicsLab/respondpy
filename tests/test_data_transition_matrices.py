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

from respondpy.data.transition_matrices import (
    _ensure_no_duplicate_keys,
    _require_columns,
    combine_dataframes,
    update_retention_probability,
    verify_transition_probability,
)


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


@pytest.mark.unit
def test_require_columns_raises_on_missing_columns() -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        _require_columns(pl.DataFrame({"a": [1]}), ["a", "b"])


@pytest.mark.unit
def test_ensure_no_duplicate_keys_handles_lazyframe() -> None:
    dup = pl.LazyFrame({"k": [1, 1], "v": [10, 10]})
    with pytest.raises(ValueError, match="Duplicate transition rows found"):
        _ensure_no_duplicate_keys(dup, ["k", "v"])


@pytest.mark.unit
def test_combine_dataframes_requires_compatible_schema() -> None:
    complete = pl.LazyFrame({"sample": [1], "time": [1], "probability": [0.0]})
    raw = pl.LazyFrame({"missing_col": [1], "probability": [0.5]})

    with pytest.raises(ValueError, match="must contain a subset of columns"):
        combine_dataframes(complete, raw).collect()


@pytest.mark.unit
def test_update_retention_probability_completes_missing_rows() -> None:
    # Missing the retention row for initial_behavior == new_behavior == "Y".
    partial = pl.DataFrame(
        {
            "sample": [1, 1, 1],
            "time": [1, 1, 1],
            "initial_intervention": ["A", "A", "A"],
            "new_intervention": ["A", "A", "A"],
            "initial_behavior": ["X", "X", "Y"],
            "new_behavior": ["X", "Y", "X"],
            "probability": [0.6, 0.4, 0.1],
        }
    )

    updated = update_retention_probability(
        partial,
        ["initial_intervention", "initial_behavior"],
        ["new_intervention", "new_behavior"],
    )

    assert updated.height == 4
    retention_y = updated.filter(
        (pl.col("initial_behavior") == "Y")
        & (pl.col("new_behavior") == "Y")
    )["probability"].item()
    assert retention_y == pytest.approx(0.9)
    assert verify_transition_probability(
        updated,
        ["initial_intervention", "initial_behavior"],
    )


@pytest.mark.unit
def test_update_retention_probability_with_custom_group_columns() -> None:
    custom = pl.DataFrame(
        {
            "cohort": [1, 1, 1, 1],
            "src": ["A", "A", "B", "B"],
            "dst": ["A", "B", "A", "B"],
            "probability": [0.0, 0.2, 0.7, 0.0],
        }
    )

    updated = update_retention_probability(
        custom,
        "src",
        "dst",
        group_columns=["cohort", "src"],
        unique_key_columns=["cohort", "src", "dst"],
    )

    assert updated.filter((pl.col("src") == "A") & (pl.col("dst") == "A"))[
        "probability"].item() == pytest.approx(0.8)
    assert updated.filter((pl.col("src") == "B") & (pl.col("dst") == "B"))[
        "probability"].item() == pytest.approx(0.3)


@pytest.mark.unit
def test_verify_transition_probability_false_when_rows_do_not_sum_to_one() -> None:
    not_normalized = pl.DataFrame(
        {
            "sample": [1, 1],
            "time": [1, 1],
            "initial_intervention": ["A", "A"],
            "new_intervention": ["A", "B"],
            "initial_behavior": ["X", "X"],
            "new_behavior": ["X", "X"],
            "probability": [0.2, 0.2],
        }
    )

    assert not verify_transition_probability(
        not_normalized,
        ["initial_intervention", "initial_behavior"],
    )
