################################################################################
# File: database_helpers.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-11-12                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl


def _normalize_state_pairs(
    values: list[tuple[int, str]] | list[list],
) -> list[tuple[int, str]]:
    """Normalize state id/name mappings to ``[(id, name), ...]`` format."""
    if not values:
        return []

    first = values[0]
    if isinstance(first, tuple) and len(first) == 2:
        return values  # type: ignore[return-value]

    # Legacy shape: [[id1, id2, ...], [name1, name2, ...]]
    if (
        len(values) == 2
        and isinstance(values[0], list)
        and isinstance(values[1], list)
        and len(values[0]) == len(values[1])
    ):
        return list(zip(values[0], values[1], strict=True))

    raise ValueError(
        "Invalid state mapping format. Expected list of (id, name) pairs."
    )


def _sort_state_vector(
    lf: pl.LazyFrame,
    behaviors: list[tuple[int, str]],
    interventions: list[tuple[int, str]],
) -> pl.LazyFrame:
    """Sort a state-vector dataframe by intervention and behavior ids.

    Parameters
    ----------
    lf : polars.LazyFrame
        State-vector LazyFrame with ``intervention`` and ``behavior``.
    behaviors : list of tuple of (int, str)
        Ordered ``(id, name)`` behavior tuples.
    interventions : list of tuple of (int, str)
        Ordered ``(id, name)`` intervention tuples.

    Returns
    -------
    polars.LazyFrame
        Sorted LazyFrame in deterministic state order.

    Raises
    ------
    ValueError
        If required state columns are missing.
    """
    s = lf.collect_schema().names()
    if "intervention" not in s or "behavior" not in s:
        raise ValueError(
            f"Invalid columns provided when attempting to sort state vector: {s}"
        )
    behavior_pairs = _normalize_state_pairs(behaviors)
    intervention_pairs = _normalize_state_pairs(interventions)

    behav = pl.LazyFrame(
        behavior_pairs, schema=["b_id", "b_name"], orient="row"
    )

    inter = pl.LazyFrame(
        intervention_pairs, schema=["i_id", "i_name"], orient="row"
    )

    # Sort by intervention id, then behavior id to match Input.get_state_names.
    sorted_lf = (
        lf.join(behav, left_on="behavior", right_on="b_name", how="inner")
        .join(inter, left_on="intervention", right_on="i_name", how="inner")
        .sort(["i_id", "b_id"])
        .drop(["i_id", "b_id"])
    )

    # Preserve the original column order to avoid accidental schema drift.
    return sorted_lf.select(s)


def _sort_transition_matrix(
    lf: pl.LazyFrame,
    behaviors: list[tuple[int, str]],
    interventions: list[tuple[int, str]],
) -> pl.LazyFrame:
    """Sort a transition-matrix dataframe into deterministic state order.

    Parameters
    ----------
    lf : polars.LazyFrame
        Transition LazyFrame with initial and next state columns.
    behaviors : list of tuple of (int, str)
        Ordered ``(id, name)`` behavior tuples.
    interventions : list of tuple of (int, str)
        Ordered ``(id, name)`` intervention tuples.

    Returns
    -------
    polars.LazyFrame
        Sorted LazyFrame for stable downstream reshaping/comparison.

    Raises
    ------
    ValueError
        If required transition columns are missing.
    """
    s = lf.collect_schema().names()
    cols = set(s)
    canonical_required = {
        "initial_intervention",
        "initial_behavior",
        "new_intervention",
        "new_behavior",
    }

    if canonical_required.issubset(cols):
        working = lf
    else:
        raise ValueError(
            f"Invalid columns provided when attempting to sort transition matrix: {s}"
        )

    behavior_pairs = _normalize_state_pairs(behaviors)
    intervention_pairs = _normalize_state_pairs(interventions)
    behavior_ids = {name: identifier for identifier, name in behavior_pairs}
    intervention_ids = {
        name: identifier for identifier, name in intervention_pairs
    }

    known_states = (
        pl.col("new_intervention").is_in(list(intervention_ids))
        & pl.col("new_behavior").is_in(list(behavior_ids))
        & pl.col("initial_intervention").is_in(list(intervention_ids))
        & pl.col("initial_behavior").is_in(list(behavior_ids))
    )

    sorted_lf = (
        lf.filter(known_states)
        .with_columns(
            pl.col("new_intervention")
            .replace_strict(intervention_ids, return_dtype=pl.Int64)
            .alias("_new_i_id"),
            pl.col("new_behavior")
            .replace_strict(behavior_ids, return_dtype=pl.Int64)
            .alias("_new_b_id"),
            pl.col("initial_intervention")
            .replace_strict(intervention_ids, return_dtype=pl.Int64)
            .alias("_initial_i_id"),
            pl.col("initial_behavior")
            .replace_strict(behavior_ids, return_dtype=pl.Int64)
            .alias("_initial_b_id"),
        )
        .sort(["_new_i_id", "_new_b_id", "_initial_i_id", "_initial_b_id"])
        .drop(
            [
                "_new_i_id",
                "_new_b_id",
                "_initial_i_id",
                "_initial_b_id",
            ]
        )
    )

    return sorted_lf.select(s)


def sort_dataframes(
    lf: pl.LazyFrame,
    behaviors: list[tuple[int, str]],
    interventions: list[tuple[int, str]],
) -> pl.LazyFrame:
    """Sort known RESPOND shapes while leaving other schemas unchanged.

    Dataframes with 3 columns are treated as state vectors, and dataframes with
    4 columns as transition matrices.

    Parameters
    ----------
    lf : polars.LazyFrame
        LazyFrame to sort.
    behaviors : list of tuple of (int, str)
        Ordered ``(id, name)`` behavior tuples.
    interventions : list of tuple of (int, str)
        Ordered ``(id, name)`` intervention tuples.

    Returns
    -------
    polars.LazyFrame
        Sorted LazyFrame when shape is recognized, otherwise input.
    """
    cols = set(lf.collect_schema().names())

    if {
        "initial_intervention",
        "initial_behavior",
        "new_intervention",
        "new_behavior",
    }.issubset(cols):
        return _sort_transition_matrix(lf, behaviors, interventions)

    if {"intervention", "behavior"}.issubset(cols):
        return _sort_state_vector(lf, behaviors, interventions)

    return lf


def get_column_order(col_name: str, values: list[str]) -> str:
    """Get the SQL ORDER BY clause for a given column and list of values.

    Parameters
    ----------
    col_name : str
        Column expression used in generated CASE conditions.
    values : list of str
        Ordered values representing desired sort priority.

    Returns
    -------
    str
        SQL CASE expression suitable for ORDER BY clauses.
    """
    order_clause = "CASE\n"
    for idx, v in enumerate(values):
        order_clause += f"WHEN {col_name} = '{v}' THEN {idx}\n"
    order_clause += f"ELSE {len(values)}\n END"
    return order_clause
