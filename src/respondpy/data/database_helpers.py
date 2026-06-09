################################################################################
# File: database_helpers.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
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
    """Sorting function for a state vector. Expects the columns ['intervention' 'behavior'].

    Args:
        lf (pl.LazyFrame): A sorted LazyFrame
        db (str | Path): A path to the database file.

    Raises:
        ValueError: Invalid column names.

    Returns:
        pl.LazyFrame: A sorted LazyFrame (sorted by intervention, behavior).
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
    ).sort(pl.col("b_id")).drop("b_id").join(
        inter, left_on="intervention", right_on="i_name", how="inner"
    ).sort(pl.col("i_id")).drop("i_id")


def _sort_transition_matrix(
    lf: pl.LazyFrame,
    behaviors: list[tuple[int, str]],
    interventions: list[tuple[int, str]]
) -> pl.LazyFrame:
    """Sorting function for the transition matrix. It expects the columns ['intervention', 'behavior', 'next_intervention', 'next_behavior']

    Args:
        lf (pl.LazyFrame): The LazyFrame to sort.
        db (str | Path): A path to the database file.

    Raises:
        ValueError: Invalid column names.

    Returns:
        pl.LazyFrame: A sorted LazyFrame (sorted by intervention, behavior, next_intervention, next_behavior).
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
    """Generalized sorting function to direct the sorting order. Only LazyFrames with state vectors (3 columns) or transition matrices (4 columns)are sorted, all other LazyFrames are returned as is.

    Args:
        lf (pl.LazyFrame): LazyFrame to sort.
        db (str | Path): A path to the database file.

    Returns:
        pl.LazyFrame: A sorted LazyFrame.
    """
    if len(lf.collect_schema().names()) == 3:
        return _sort_state_vector(lf, behaviors, interventions)
    if len(lf.collect_schema().names()) == 4:
        return _sort_transition_matrix(lf, behaviors, interventions)
    return lf


def get_column_order(col_name: str, values: list[str]) -> str:
    """Get the SQL ORDER BY clause for a given column and list of values.

    Args:
        col_name (str): column in the SQLite table to order by.
        values (list[str]): List of values to order by.

    Returns:
        str: String representing the SQL ORDER BY clause.
    """
    order_clause = "CASE\n"
    for idx, v in enumerate(values):
        order_clause += f"WHEN {col_name} = \'{v}\' THEN {idx}\n"
    order_clause += f"ELSE {len(values)}\n END"
    return order_clause
