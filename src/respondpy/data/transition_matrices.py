################################################################################
# File: transition_matrices.py                                                 #
# Project: respondpy                                                           #
# Created Date: 2026-06-02                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl

from .parameters import Parameter, ParameterType


def _require_columns(frame: pl.DataFrame, columns: list[str]) -> None:
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def _validate_probability_column(
    frame: pl.DataFrame,
    probability_column: str,
) -> None:
    _require_columns(frame, [probability_column])
    has_null = frame.select(pl.col(probability_column).is_null().any()).item()
    if has_null:
        raise ValueError(f"Null values found in {probability_column}")


def _ensure_no_duplicate_keys(frame: pl.DataFrame, key_columns: list[str]) -> None:
    _require_columns(frame, key_columns)
    has_duplicates = frame.select(
        pl.struct(key_columns).is_duplicated().any()).item()
    if has_duplicates:
        raise ValueError(
            f"Duplicate transition rows found for key columns: {key_columns}"
        )


def _infer_transition_shape(
    frame: pl.DataFrame,
) -> tuple[list[str], str, str, list[str]]:
    intervention_cols = {
        "sample",
        "time",
        "initial_intervention",
        "new_intervention",
        "behavior",
    }
    behavior_cols = {
        "sample",
        "time",
        "intervention",
        "initial_behavior",
        "new_behavior",
    }

    cols = set(frame.columns)
    if intervention_cols.issubset(cols):
        group_columns = ["sample", "time", "initial_intervention", "behavior"]
        origin_column = "initial_intervention"
        destination_column = "new_intervention"
        unique_key_columns = group_columns + [destination_column]
        return group_columns, origin_column, destination_column, unique_key_columns

    if behavior_cols.issubset(cols):
        group_columns = ["sample", "time", "intervention", "initial_behavior"]
        origin_column = "initial_behavior"
        destination_column = "new_behavior"
        unique_key_columns = group_columns + [destination_column]
        return group_columns, origin_column, destination_column, unique_key_columns

    raise ValueError(
        "Unable to infer transition shape from columns. Expected intervention or behavior transition matrix columns."
    )


def _complete_transition_rows(
    transition_matrix: pl.DataFrame,
    group_columns: list[str],
    origin_column: str,
    destination_column: str,
    *,
    probability_column: str = "probability",
) -> pl.DataFrame:
    group_without_origin = [c for c in group_columns if c != origin_column]
    transition_keys = group_without_origin + \
        [origin_column, destination_column]

    all_states = pl.concat(
        [
            transition_matrix.select(pl.col(origin_column).alias("_state")),
            transition_matrix.select(
                pl.col(destination_column).alias("_state")),
        ]
    ).unique()

    strata = transition_matrix.select(group_without_origin).unique()
    complete_keyspace = (
        strata.join(
            all_states.rename({"_state": origin_column}),
            how="cross",
        )
        .join(
            all_states.rename({"_state": destination_column}),
            how="cross",
        )
    )

    return (
        complete_keyspace.join(
            transition_matrix.select(transition_keys + [probability_column]),
            on=transition_keys,
            how="left",
        )
        .with_columns(pl.col(probability_column).fill_null(0.0))
        .select(group_columns + [destination_column, probability_column])
    )

# Welp, right now this is struggling because by nature a markov transition matrix is square. However, because we have transition operations we have a bit of a different behavior resulting in half matrices. This is because there is only one way movement in each transition operation and so we'd have duplcate column values in the "next" columns (e.g. intervention transitions would duplicate the behavior states). Gotta think more about this one.


def _build_filled_intervention_matrix(
        interventions: list[str],
        behaviors: list[str],
        *,
        sample_id: int = 1,
        time: int = 1,
        constant: float = 0.0
) -> pl.DataFrame:
    inter = pl.DataFrame({"initial_intervention": interventions})
    new_inter = pl.DataFrame({"new_intervention": interventions})
    behav = pl.DataFrame({"behavior": behaviors})

    return (
        inter
        .join(new_inter, how="cross")
        .join(behav, how="cross")
        .with_columns(
            sample=pl.lit(sample_id),
            time=pl.lit(time),
            probability=pl.lit(constant),
        )
        .select(
            [
                "sample",
                "time",
                "initial_intervention",
                "new_intervention",
                "behavior",
                "probability",
            ]
        )
    )


def _build_filled_behavior_matrix(
        interventions: list[str],
        behaviors: list[str],
        *,
        sample_id: int = 1,
        time: int = 1,
        constant: float = 0.0
) -> pl.DataFrame:
    behav = pl.DataFrame({"initial_behavior": behaviors})
    new_behav = pl.DataFrame({"new_behavior": behaviors})
    inter = pl.DataFrame({"intervention": interventions})

    return (
        behav
        .join(new_behav, how="cross")
        .join(inter, how="cross")
        .with_columns(
            sample=pl.lit(sample_id),
            time=pl.lit(time),
            probability=pl.lit(constant),
        )
        .select(
            [
                "sample",
                "time",
                "initial_behavior",
                "new_behavior",
                "intervention",
                "probability",
            ]
        )
    )


def build_constant_transition(
    parameter: Parameter,
    interventions: list[str],
    behaviors: list[str],
    *,
    sample_id: int = 1,
    time: int = 1,
    constant: float = 0.0
) -> pl.DataFrame:
    if parameter == ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
        return _build_filled_intervention_matrix(
            interventions,
            behaviors,
            sample_id=sample_id,
            time=time,
            constant=constant,
        )
    if parameter == ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
        return _build_filled_behavior_matrix(
            interventions,
            behaviors,
            sample_id=sample_id,
            time=time,
            constant=constant,
        )
    raise ValueError(
        f"ParameterType {parameter} is not a valid state transition parameter."
    )


def update_retention_probability(
    transition_matrix: pl.DataFrame,
    transition_column: str,
    new_column: str,
    *,
    probability_column: str = "probability",
    group_columns: list[str] | None = None,
    unique_key_columns: list[str] | None = None,
    retention_pairs: list[tuple[str, str]] | None = None,
    complete_missing: bool = True,
    tolerance: float = 1e-12,
    forbid_negative_retention: bool = True,
) -> pl.DataFrame:
    inferred_group_columns, inferred_origin, inferred_destination, inferred_unique_keys = (
        _infer_transition_shape(transition_matrix)
        if group_columns is None
        else (group_columns, transition_column, new_column, [])
    )

    active_group_columns = group_columns or inferred_group_columns
    origin_column = inferred_origin if group_columns is None else transition_column
    destination_column = inferred_destination if group_columns is None else new_column
    active_unique_keys = unique_key_columns or inferred_unique_keys
    if not active_unique_keys:
        active_unique_keys = active_group_columns + [destination_column]

    active_retention_pairs = retention_pairs or [
        (origin_column, destination_column)]

    _require_columns(
        transition_matrix,
        active_group_columns + [origin_column, destination_column],
    )
    _require_columns(
        transition_matrix,
        [c for pair in active_retention_pairs for c in pair],
    )
    _validate_probability_column(transition_matrix, probability_column)
    _ensure_no_duplicate_keys(transition_matrix, active_unique_keys)

    if complete_missing:
        completed = _complete_transition_rows(
            transition_matrix,
            active_group_columns,
            origin_column,
            destination_column,
            probability_column=probability_column,
        )
    else:
        completed = transition_matrix

    is_retention = pl.lit(True)
    for origin_col, destination_col in active_retention_pairs:
        is_retention = is_retention & (
            pl.col(destination_col) == pl.col(origin_col)
        )

    non_retention = (
        completed
        .filter(~is_retention)
        .group_by(active_group_columns)
        .agg(pl.col(probability_column).sum().alias("__non_retention_sum"))
    )

    retention_targets = (
        completed.select(active_group_columns)
        .unique()
        .join(non_retention, on=active_group_columns, how="left")
        .with_columns(
            pl.col("__non_retention_sum").fill_null(0.0),
            (1.0 - pl.col("__non_retention_sum")).alias("__retention_target"),
        )
        .drop("__non_retention_sum")
    )

    if forbid_negative_retention:
        has_negative = retention_targets.select(
            pl.col("__retention_target").lt(-tolerance).any()
        ).item()
        if has_negative:
            raise ValueError(
                "Cannot update retention probabilities: non-retention probabilities exceed 1 in at least one transition group."
            )

    retention_targets = retention_targets.with_columns(
        pl.when(pl.col("__retention_target").abs().le(tolerance))
        .then(0.0)
        .otherwise(pl.col("__retention_target"))
        .alias("__retention_target")
    )

    result = (
        completed.join(retention_targets, on=active_group_columns, how="left")
        .with_columns(
            pl.when(is_retention)
            .then(pl.col("__retention_target"))
            .otherwise(pl.col(probability_column))
            .alias(probability_column)
        )
        .drop("__retention_target")
    )

    # final invariant check; this keeps the function idempotent and defensive
    if not verify_transition_probability(
        result,
        origin_column,
        probability_column=probability_column,
        group_columns=active_group_columns,
        unique_key_columns=active_unique_keys,
        tolerance=tolerance,
    ):
        raise ValueError(
            "Retention update failed to normalize probabilities to 1 for all transition groups."
        )

    return result


def verify_transition_probability(
    transition_matrix: pl.DataFrame,
    transition_column: str,
    *,
    probability_column: str = "probability",
    group_columns: list[str] | None = None,
    unique_key_columns: list[str] | None = None,
    tolerance: float = 1e-12,
) -> bool:
    """Checks that the transition probabilities that correspond to movement from the initial state sum to one.

    Args:
        transition_matrix (pl.DataFrame): _description_

    Returns:
        bool: _description_
    """
    inferred_group_columns, _, destination_column, inferred_unique_keys = (
        _infer_transition_shape(transition_matrix)
        if group_columns is None
        else (group_columns, transition_column, "", [])
    )
    active_group_columns = group_columns or inferred_group_columns
    active_unique_keys = unique_key_columns or inferred_unique_keys
    if not active_unique_keys and destination_column:
        active_unique_keys = active_group_columns + [destination_column]
    if not active_unique_keys:
        active_unique_keys = [
            c for c in transition_matrix.columns if c != probability_column
        ]

    _require_columns(transition_matrix, active_group_columns)
    _validate_probability_column(transition_matrix, probability_column)
    _ensure_no_duplicate_keys(transition_matrix, active_unique_keys)

    grouped = transition_matrix.group_by(active_group_columns).agg(
        pl.col(probability_column).sum().alias("prob_sum")
    )

    return grouped.select(
        (pl.col("prob_sum") - 1.0).abs().le(tolerance).all()
    ).item()
