################################################################################
# File: test_data_database_helpers.py                                          #
# Project: respondpy                                                           #
# Created Date: 2026-06-10                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-17                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################


from __future__ import annotations

import polars as pl
import pytest

import respondpy.data as rpydata
from respondpy.data.database_helpers import (
    _sort_state_vector,
    _sort_transition_matrix,
    get_column_order,
    sort_dataframes,
)


@pytest.mark.unit
def test_data_module_dir_matches_exports() -> None:
    assert sorted(rpydata.__dir__()) == sorted(rpydata.__all__)


@pytest.mark.unit
def test_validate_time_list_removes_initial_timestep() -> None:
    assert rpydata.validate_time_list([1, 52, 104]) == [52, 104]


@pytest.mark.unit
def test_validate_time_list_rejects_non_positive_values() -> None:
    with pytest.raises(ValueError, match="zero or a negative number"):
        rpydata.validate_time_list([52, 0])


@pytest.mark.unit
def test_sort_transition_matrix_requires_columns() -> None:
    with pytest.raises(ValueError, match="Invalid columns provided"):
        _sort_transition_matrix(
            pl.DataFrame(
                {"foo": [1], "bar": [2], "baz": [3], "probability": [0.1]}
            ),
            [(1, "b1")],
            [(1, "i1")],
        )


@pytest.mark.unit
def test_get_column_order_builds_case_clause() -> None:
    clause = get_column_order("i.name", ["no_treatment", "buprenorphine"])
    assert "WHEN i.name = 'no_treatment' THEN 0" in clause
    assert "WHEN i.name = 'buprenorphine' THEN 1" in clause
    assert "ELSE 2" in clause


@pytest.mark.unit
def test_sort_dataframes_unrecognized_shape_returns_input() -> None:
    lf = pl.LazyFrame({"a": [1], "b": [2]})
    out = sort_dataframes(lf, [(1, "b1")], [(1, "i1")]).collect()
    assert out.columns == ["a", "b"]
    assert out.row(0) == (1, 2)


@pytest.mark.unit
def test_sort_state_vector_requires_columns() -> None:
    with pytest.raises(ValueError, match="Invalid columns provided"):
        _sort_state_vector(
            pl.LazyFrame({"foo": [1], "bar": [2], "count": [3]}),
            [(1, "b1")],
            [(1, "i1")],
        ).collect()


@pytest.mark.unit
def test_sort_state_vector_happy_path() -> None:
    lf = pl.LazyFrame(
        {
            "intervention": ["i2", "i1", "i2", "i1"],
            "behavior": ["b2", "b2", "b1", "b1"],
            "count": [40, 20, 30, 10],
        }
    )

    out = _sort_state_vector(
        lf,
        behaviors=[(1, "b1"), (2, "b2")],
        interventions=[(1, "i1"), (2, "i2")],
    ).collect()

    assert out.columns == ["intervention", "behavior", "count"]
    assert out.select("count").to_series().to_list() == [10, 20, 30, 40]


@pytest.mark.unit
@pytest.mark.filterwarnings(
    "ignore:Determining the column names of a LazyFrame requires resolving its schema.*:polars.exceptions.PerformanceWarning"
)
def test_sort_transition_matrix_happy_path() -> None:
    lf = pl.LazyFrame(
        {
            "intervention": ["i2", "i1", "i2", "i1"],
            "behavior": ["b2", "b1", "b1", "b2"],
            "next_intervention": ["i1", "i2", "i2", "i1"],
            "next_behavior": ["b1", "b2", "b1", "b2"],
            "probability": [0.1, 0.2, 0.3, 0.4],
            # Current implementation drops this column before re-adding it.
            "i_id": [0, 0, 0, 0],
        }
    )

    out = _sort_transition_matrix(
        lf,
        behaviors=[[1, 2], ["b1", "b2"]],
        interventions=[[1, 2], ["i1", "i2"]],
    ).collect()

    assert out.height == 4
    assert "probability" in out.columns


@pytest.mark.unit
def test_sort_dataframes_calls_state_vector_sort(monkeypatch: pytest.MonkeyPatch) -> None:
    lf = pl.LazyFrame(
        {
            "intervention": ["i1"],
            "behavior": ["b1"],
            "count": [1.0],
        }
    )

    def fake_sort_state_vector(
            _lf: pl.LazyFrame,
            _behaviors: list[tuple[int, str]],
            _interventions: list[tuple[int, str]],
    ) -> pl.LazyFrame:
        return pl.LazyFrame({"sentinel": [1]})

    monkeypatch.setattr(
        "respondpy.data.database_helpers._sort_state_vector",
        fake_sort_state_vector,
    )

    out = sort_dataframes(lf, [(1, "b1")], [(1, "i1")]).collect()
    assert out.columns == ["sentinel"]


@pytest.mark.unit
def test_sort_dataframes_calls_transition_matrix_sort(monkeypatch: pytest.MonkeyPatch) -> None:
    lf = pl.LazyFrame(
        {
            "intervention": ["i1"],
            "behavior": ["b1"],
            "next_intervention": ["i1"],
            "next_behavior": ["b1"],
        }
    )

    def fake_sort_transition_matrix(
            _lf: pl.LazyFrame,
            _behaviors: list[tuple[int, str]],
            _interventions: list[tuple[int, str]],
    ) -> pl.LazyFrame:
        return pl.LazyFrame({"sentinel": [2]})

    monkeypatch.setattr(
        "respondpy.data.database_helpers._sort_transition_matrix",
        fake_sort_transition_matrix,
    )

    out = sort_dataframes(lf, [(1, "b1")], [(1, "i1")]).collect()
    assert out.columns == ["sentinel"]
