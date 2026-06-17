################################################################################
# File: transition_matrices.py                                                 #
# Project: respondpy                                                           #
# Created Date: 2026-06-02                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-10                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl
import numpy as np

def _require_columns(
        frame: pl.LazyFrame | pl.DataFrame, columns: list[str]
) -> None:
    if isinstance(frame, pl.LazyFrame):
        frame_cols = set(frame.collect_schema().names())
    else:
        frame_cols = set(frame.columns)
    missing = [c for c in columns if c not in frame_cols]
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


def _ensure_no_duplicate_keys(
        frame: pl.LazyFrame | pl.DataFrame,
        key_columns: list[str] | None = None
) -> None:
    if not key_columns:
        key_columns = frame.collect_schema().names()
    else:
        _require_columns(frame, key_columns)

    # We have to collect because we need to verify the contents of the dataframe
    if isinstance(frame, pl.LazyFrame):
        frame = frame.collect()
    has_duplicates = frame.select(
        pl.struct(key_columns).is_duplicated().any()).item()
    if has_duplicates:
        raise ValueError(
            f"Duplicate transition rows found for key columns: {key_columns}"
        )


def _default_transition_shape(
    frame: pl.LazyFrame | pl.DataFrame,
) -> tuple[list[str], list[str], list[str], list[str]]:
    default_cols = {
        "sample",
        "time",
        "initial_intervention",
        "new_intervention",
        "initial_behavior",
        "new_behavior"
    }

    if isinstance(frame, pl.LazyFrame):
        cols = set(frame.collect_schema().names())
    else:
        cols = set(frame.columns)

    if default_cols.issubset(cols):
        from_cols = ['initial_intervention', 'initial_behavior']
        to_cols = ['new_intervention', 'new_behavior']
        sample_cols = ["sample", "time"]
        grouping_cols = sample_cols + from_cols
        unique_conditions = sample_cols + from_cols + to_cols
        return grouping_cols, from_cols, to_cols, unique_conditions

    raise ValueError("Unable to find default transition shape in columns.")


def build_constant_transition(
    interventions: list[str],
    behaviors: list[str],
    *,
    sample_id: int = 1,
    time: int = 1,
    constant: float = 0.0
) -> pl.LazyFrame:
    """Build a complete constant-valued transition matrix table.

    :param interventions: Ordered intervention names.
    :param behaviors: Ordered behavior names.
    :param sample_id: Sample identifier written into output rows.
    :param time: Timestep written into output rows.
    :param constant: Constant probability assigned before normalization.
    :returns: LazyFrame containing all from/to state combinations.
    :raises ValueError: If the generated matrix is not square.
    """
    init_behav = pl.LazyFrame({"initial_behavior": behaviors})
    new_behav = pl.LazyFrame({"new_behavior": behaviors})
    init_inter = pl.LazyFrame({"initial_intervention": interventions})
    new_inter = pl.LazyFrame({"new_intervention": interventions})

    result = init_behav.join(
        new_behav, how="cross"
    ).join(
        init_inter, how="cross"
    ).join(
        new_inter, how="cross"
    ).with_columns(
        sample=pl.lit(sample_id),
        time=pl.lit(time),
        probability=pl.lit(constant),
    ).select(
        [
            "sample",
            "time",
            "initial_behavior",
            "new_behavior",
            "initial_intervention",
            "new_intervention",
            "probability",
        ]
    )

    n_states = len(interventions) * len(behaviors)

    if result.select(pl.len()).collect().item() != n_states**2:
        raise ValueError(
            "The resulting transition matrix is not square. Check that the number of interventions and behaviors is correct."
        )

    return result


def combine_dataframes(
        complete_df: pl.LazyFrame,
        raw_data_df: pl.LazyFrame,
        *,
        value_col: str = "probability"
) -> pl.LazyFrame:
    """Overlay raw sampled values onto a complete template dataframe.

    Values in ``raw_data_df`` take precedence over template values where keys
    match.

    :param complete_df: Fully enumerated dataframe used as fallback.
    :param raw_data_df: Observed values to merge into template.
    :param value_col: Name of numeric value column to collapse.
    :returns: Combined LazyFrame with a single ``value_col``.
    :raises ValueError: If join key columns are incompatible.
    """
    join_cols = raw_data_df.collect_schema().names()
    join_cols.remove(value_col)
    if not set(
        join_cols
    ).issubset(set(complete_df.collect_schema().names())):
        raise ValueError(
            f"The raw data dataframe must contain a subset of columns of the complete dataframe in order to combine them! Complete dataframe columns: {complete_df.collect_schema().names()}, raw data dataframe columns: {raw_data_df.collect_schema().names()}"
        )
    # We want to join on all columns except the value column, and then collapse the value column so that if there is a value in raw_data_df it takes precedence, but if there isn't then we keep the value from complete_df. This allows us to fill in missing values with the constant dataframes.
    joined_lf = complete_df.join(
        raw_data_df, on=join_cols, how="left", suffix="_new")
    collapsed_df = joined_lf.with_columns(
        pl.when(
            pl.col(f"{value_col}_new").is_null()
        ).then(
            pl.col(value_col)
        ).otherwise(
            pl.col(f"{value_col}_new")
        ).alias(value_col)
    ).select(pl.all().exclude(f"{value_col}_new"))
    return collapsed_df


def update_retention_probability(
    transition_matrix: pl.LazyFrame | pl.DataFrame,
    transition_columns: str | list[str],
    new_columns: str | list[str],
    *,
    probability_column: str = "probability",
    group_columns: list[str] | None = None,
    unique_key_columns: list[str] | None = None,
    tolerance: float = 1e-12,
    forbid_negative_retention: bool = True,
) -> pl.DataFrame:
    """Set retention probabilities so each transition group sums to one.

    Retention rows are those where origin-state columns equal destination-state
    columns. Their values are replaced by ``1 - sum(non_retention)`` per group.

    :param transition_matrix: Transition rows to normalize.
    :param transition_columns: Origin-state column(s).
    :param new_columns: Destination-state column(s).
    :param probability_column: Probability column to update.
    :param group_columns: Grouping keys defining one origin state/time/sample.
    :param unique_key_columns: Columns expected to uniquely identify rows.
    :param tolerance: Floating-point tolerance for validation checks.
    :param forbid_negative_retention: If ``True``, reject negative retention.
    :returns: Transition dataframe with updated retention probabilities.
    :raises ValueError: If schema validation fails or probabilities cannot be
        normalized.
    """
    if group_columns is None or unique_key_columns is None:
        group_cols, from_cols, to_cols, constraints = _default_transition_shape(
            transition_matrix)
    else:
        group_cols = group_columns
        from_cols = transition_columns if isinstance(
            transition_columns, list) else [transition_columns]
        to_cols = new_columns if isinstance(
            new_columns, list) else [new_columns]
        constraints = []

    _require_columns(transition_matrix, constraints + [probability_column])
    _ensure_no_duplicate_keys(transition_matrix, constraints)

    if len(to_cols) != len(from_cols):
        raise ValueError(
            "The number of transition from columns does not match the number of transition to columns!")

    # we have to collect the LazyFrame here because we need to count rows
    if isinstance(transition_matrix, pl.LazyFrame):
        transition_matrix = transition_matrix.collect()

    n_states = np.square(
        np.prod([transition_matrix.n_unique(c) for c in from_cols])
    )

    if transition_matrix.select(pl.len()).item() != n_states:
        required_cols = ['initial_intervention',
                         'initial_behavior', 'sample', 'time']
        if not set(required_cols).issubset(set(transition_matrix.columns)):
            raise ValueError(
                "Transition matrix is missing required columns for completion. Please provide a complete transition matrix or ensure that 'initial_intervention' and 'initial_behavior' columns are present for automatic completion."
            )
        inter = transition_matrix['initial_intervention'].unique().to_list()
        behav = transition_matrix['initial_behavior'].unique().to_list()
        sample = transition_matrix['sample'].unique().item()
        time = transition_matrix['time'].unique().item()

        completed = combine_dataframes(
            build_constant_transition(
                inter, behav, sample_id=sample, time=time
            ), transition_matrix.lazy(), value_col=probability_column).collect()
    else:
        completed = transition_matrix

    from_to_pairs = [(from_cols, to_cols)]

    _validate_probability_column(transition_matrix, probability_column)

    is_retention = pl.lit(True)
    for origin_cols, destination_cols in from_to_pairs:
        for origin_col, destination_col in zip(origin_cols, destination_cols):
            is_retention = is_retention & (
                pl.col(destination_col) == pl.col(origin_col)
            )

    non_retention = (
        completed
        .filter(~is_retention)
        .group_by(group_cols)  # Add new_behavior (if intervention)
        .agg(pl.col(probability_column).sum().alias("__non_retention_sum"))
    )

    retention_targets = (
        completed.select(group_cols)
        .unique()
        .join(non_retention, on=group_cols, how="left")
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
        completed.join(retention_targets, on=group_cols, how="left")
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
        from_cols,
        probability_column=probability_column,
        group_columns=group_cols,
        unique_key_columns=constraints,
        tolerance=tolerance,
    ):
        raise ValueError(
            "Retention update failed to normalize probabilities to 1 for all transition groups."
        )

    return result


def verify_transition_probability(
    transition_matrix: pl.DataFrame,
    transition_columns: str | list[str],
    *,
    probability_column: str = "probability",
    group_columns: list[str] | None = None,
    unique_key_columns: list[str] | None = None,
    tolerance: float = 1e-12,
) -> bool:
    """Check that transition probabilities sum to one within each group.

    :param transition_matrix: Transition rows to verify.
    :param transition_columns: Origin-state column(s), used with grouping.
    :param probability_column: Probability column to sum.
    :param group_columns: Explicit grouping keys. If omitted, defaults are
        inferred.
    :param unique_key_columns: Explicit unique-key columns. If omitted,
        defaults are inferred.
    :param tolerance: Absolute tolerance for checking sums against ``1.0``.
    :returns: ``True`` when all transition groups sum to one.
    """
    if group_columns is None or unique_key_columns is None:
        group_cols, _, _, constraints = _default_transition_shape(
            transition_matrix)
    else:
        group_cols = group_columns
        constraints = transition_matrix.columns
        constraints.remove(probability_column)

    if isinstance(transition_columns, str):
        transition_columns = [transition_columns]

    _require_columns(transition_matrix, group_cols)
    _validate_probability_column(transition_matrix, probability_column)
    _ensure_no_duplicate_keys(transition_matrix, constraints)

    grouped = transition_matrix.group_by(group_cols).agg(
        pl.col(probability_column).sum().alias("prob_sum")
    )

    return grouped.select(
        (pl.col("prob_sum") - 1.0).abs().le(tolerance).all()
    ).item()
