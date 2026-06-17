################################################################################
# File: database_helpers.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-17                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl


def _sort_state_vector(
    lf: pl.LazyFrame,
    behaviors: list[tuple[int, str]],
    interventions: list[tuple[int, str]]
) -> pl.LazyFrame:
    """Sort a state-vector dataframe by intervention and behavior ids.

    :param lf: State-vector LazyFrame with ``intervention`` and ``behavior``.
    :param behaviors: Ordered ``(id, name)`` behavior tuples.
    :param interventions: Ordered ``(id, name)`` intervention tuples.
    :returns: Sorted LazyFrame in deterministic state order.
    :raises ValueError: If required state columns are missing.
    """
    s = lf.collect_schema().names()
    if 'intervention' not in s or 'behavior' not in s:
        raise ValueError(
            f"Invalid columns provided when attempting to sort state vector: {s}")
    behav = pl.LazyFrame(
        behaviors, schema=["b_id", "b_name"], orient='row')

    inter = pl.LazyFrame(
        interventions, schema=["i_id", "i_name"], orient='row')

    # Sort first by behaviors, then by interventions
    return lf.join(
        behav, left_on="behavior", right_on="b_name", how="inner"
    ).join(
        inter, left_on="intervention", right_on="i_name", how="inner"
    ).sort(["i_id", "b_id"]).drop(["i_id", "b_id"])


def _sort_transition_matrix(
    lf: pl.LazyFrame,
    behaviors: list[tuple[int, str]],
    interventions: list[tuple[int, str]]
) -> pl.LazyFrame:
    """Sort a transition-matrix dataframe into deterministic state order.

    :param lf: Transition LazyFrame with initial and next state columns.
    :param behaviors: Ordered ``(id, name)`` behavior tuples.
    :param interventions: Ordered ``(id, name)`` intervention tuples.
    :returns: Sorted LazyFrame for stable downstream reshaping/comparison.
    :raises ValueError: If required transition columns are missing.
    """
    if 'intervention' not in lf.columns or 'behavior' not in lf.columns or 'next_intervention' not in lf.columns or 'next_behavior' not in lf.columns:
        raise ValueError(
            f"Invalid columns provided when attempting to sort transition matrix: {lf.columns}")
    behav = pl.LazyFrame(behaviors, schema=["b_id", "b_name"])
    inter = pl.LazyFrame(interventions, schema=["i_id", "i_name"])

    # Sort order:
    #   1. Next Behavior
    #   2. Next Behavior
    #   3. Initial Behavior
    #   4. Initial Intervention
    #   e.g. [active_injection, no_treatment, active_injection, no_treatment], [active_injection, no_treatment, active_injection, buprenorphine], [active_injection, no_treatment, active_injection, methadone], etc.
    return lf.drop("i_id").join(
        behav, left_on="next_behavior", right_on="b_name", how="inner"
    ).sort(pl.col("b_id")).drop("b_id").join(
        inter, left_on="next_intervention", right_on="i_name", how="inner"
    ).sort(pl.col("i_id")).drop("i_id").join(
        behav, left_on="behavior", right_on="b_name", how="inner"
    ).sort(pl.col("b_id")).drop("b_id").join(
        inter, left_on="intervention", right_on="i_name", how="inner"
    ).sort(pl.col("i_id"))


def sort_dataframes(
        lf: pl.LazyFrame,
        behaviors: list[tuple[int, str]],
        interventions: list[tuple[int, str]]
) -> pl.LazyFrame:
    """Sort known RESPOND shapes while leaving other schemas unchanged.

    Dataframes with 3 columns are treated as state vectors, and dataframes with
    4 columns as transition matrices.

    :param lf: LazyFrame to sort.
    :param behaviors: Ordered ``(id, name)`` behavior tuples.
    :param interventions: Ordered ``(id, name)`` intervention tuples.
    :returns: Sorted LazyFrame when shape is recognized, otherwise input.
    """
    if len(lf.collect_schema().names()) == 3:
        return _sort_state_vector(lf, behaviors, interventions)
    if len(lf.collect_schema().names()) == 4:
        return _sort_transition_matrix(lf, behaviors, interventions)
    return lf


def get_column_order(col_name: str, values: list[str]) -> str:
    """Get the SQL ORDER BY clause for a given column and list of values.

    :param col_name: Column expression used in generated CASE conditions.
    :param values: Ordered values representing desired sort priority.
    :returns: SQL CASE expression suitable for ORDER BY clauses.
    """
    order_clause = "CASE\n"
    for idx, v in enumerate(values):
        order_clause += f"WHEN {col_name} = \'{v}\' THEN {idx}\n"
    order_clause += f"ELSE {len(values)}\n END"
    return order_clause
