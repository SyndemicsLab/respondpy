################################################################################
# File: build_transition.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-02-26                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-02                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################
from pathlib import Path
import itertools

import polars as pl
import numpy as np

from respondpy.io.reading import get_parameter_by_id_and_time, get_state_names, get_behaviors, get_interventions, get_behavior_table, get_intervention_table
from respondpy.data.parameters import Parameter

# Internal Functions


def _validate_time(time: int | None, p: Parameter) -> int:
    """Helper function to validate a good time value for the specified parameter. If the parameter is

    Args:
        time (int | None): The time variable to check.
        p (Parameter): The parameter to validate time against.

    Raises:
        ValueError: If time is None and the parameter is not the initial cohort, warn the user they need a time.

    Returns:
        int: The parameter time or 0 if None and the parameter is an initial cohort.
    """
    if time is None:
        if p != Parameter.INITIAL_COHORT:
            raise ValueError(
                f"Parameter being extracted requires a time value be provided, but none was found: {p}")
        return 0
    return time


def _get_sample_column_string(p: Parameter) -> str:
    """Getter for the column name in cohort representing the sample ID based on the parameter specified.

    Args:
        p (Parameter): The parameter we want the column name for.

    Raises:
        ValueError: Invalid parameter specified.

    Returns:
        str: The column name in the cohort table for the parameter sample.
    """
    if p == Parameter.INITIAL_COHORT:
        return "initial_population_sample"
    if p == Parameter.MIGRATION_COHORT:
        return "population_change_sample"
    if p == Parameter.INTERVENTION_TRANSITION_PROBABILITY:
        return "intervention_transition_sample"
    if p == Parameter.BEHAVIOR_TRANSITION_PROBABILITY:
        return "behavior_transition_sample"
    if p == Parameter.OVERDOSE_PROBABILITY:
        return "overdose_sample"
    if p == Parameter.OVERDOSE_FATALITY_PROBABILITY:
        return "overdose_fatality_sample"
    if p == Parameter.STANDARD_MORTALITY_RATIO:
        return "smr_sample"
    if p == Parameter.BACKGROUND_DEATH_PROBABILITY:
        return "background_mortality_sample"
    raise ValueError(
        f"Parameter value supplied is not implemented in the cohort table! {p}.")


def _get_parameter_data(
        p: Parameter,
        db: str | Path,
        sample_ids: pl.DataFrame,
        time: int
) -> pl.LazyFrame:
    """Getter for the parameter data from the database.

    Args:
        p (Parameter): The parameter to retrieve from the database.
        db (str | Path): The path to the database file.
        sample_ids (pl.DataFrame): The cohort table containing the sample IDs.
        time (int): The time point to get data for.

    Returns:
        pl.LazyFrame: A LazyFrame containing the parameter data from the database. The columns match the columns of the select statement, a state vector returns 3 columns ['intervention', 'behavior', 'value'] pattern where a transition matrix returns 4 columns ['init_intervention', 'init_behaivor' 'next_parameter', 'value']. Constant values return the single column.
    """
    sid_name = _get_sample_column_string(p)
    ret_cols, ret_values = get_parameter_by_id_and_time(
        p, db, sample_ids.select(pl.col(sid_name)).item(), time
    )
    return pl.LazyFrame(ret_values, schema=ret_cols, orient='row')


def _fill_missing_values(
        lf: pl.LazyFrame,
        p: Parameter,
        db: str | Path,
        sample_ids: pl.DataFrame,
        time: int
) -> pl.LazyFrame:
    """Helper function to fill missing values for a sample. This is applied when we only want to draw a specific subset of values from a transition matrix and hold the rest constant (e.g. intervention transitions where we calibrate uptake and fix loss to follow up).

    Args:
        lf (pl.LazyFrame): LazyFrame containing the sampled parameters
        p (Parameter): Parameter of the data the LazyFrame contains
        db (str | Path): Path to the database file
        sample_ids (pl.DataFrame): The row of sample ids from the cohort table
        time (int): Timestep for the sampled parameters

    Raises:
        ValueError: Too many transitions found in the sample
        ValueError: The first sample does not have fixed values

    Returns:
        pl.LazyFrame: A set of data composed of both fixed and sampled parameters. A state vector returns a 3 column ['intervention', 'behavior', 'value'] pattern where a transition matrix returns 4 columns ['init_intervention', 'init_behavior' 'next_parameter', 'value']. Constant values return the single column.
    """
    # quick exit if background mortality since it is a cohort constant
    if p == Parameter.BACKGROUND_DEATH_PROBABILITY:
        return lf
    sid_name = _get_sample_column_string(p)

    num_states = len(get_state_names(db))
    if p == Parameter.INTERVENTION_TRANSITION_PROBABILITY:
        num_states *= len(get_interventions(db))
        # check the height of a dataframe is the size of the intervention list in the db
    elif p == Parameter.BEHAVIOR_TRANSITION_PROBABILITY:
        num_states *= len(get_behaviors(db))
        # check the height of a dataframe is the size of the behavior list in the db

    sample_id = sample_ids.select(pl.col(sid_name)).item()
    height = lf.collect().height
    if height == num_states:
        return lf
    if height > num_states:
        raise ValueError(
            f"Too many transition values found for sample {sample_id} and parameter {p}")

    # Below assumes the dataframe has only part of the data and we must load more from fixed samples
    if sample_id == 1:
        raise ValueError(
            f"The first sample in the database for parameter {p} does not have {num_states} values!")
    one_cols, one_values = get_parameter_by_id_and_time(p, db, 1, time)
    return _fill_gaps_with_sample(lf, pl.LazyFrame(one_values, schema=one_cols, orient='row'))


def _build_transition_matrix_from_partial(
        partial: pl.LazyFrame,
        db: str | Path,
        *,
        on_cols: list | None = None
) -> pl.LazyFrame:
    """Helper function to build a transition matrix from the samples. This only executes if the partial has 4 columns (the indicator for a transition matrix). This function is needed because both transition matrices (interventions and behaviors) are sparse matrices.

    Note: partial has columns dependent on the parameter, but the only transition matrices are intervention and behavior. Thus the columns must be either:
        - ['initial_intervention', 'new_intervention', 'behavior', 'probability']
        - ['intervention', 'initial_behavior', 'new_behavior', 'probability']

    Args:
        partial (pl.LazyFrame): The sample from the database with both sampled and fixed values.
        db (str | Path): A path to the database file.
        on_cols (list | None, optional): What columns to join on. If None is provided, defaults to ['intervention', 'behavior'].

    Raises:
        ValueError: Invalid number of column names have the "new_" prefix.
        NotImplementedError: A column other than intervention or behavior has the "new_" prefix.

    Returns:
        pl.LazyFrame: Either the original partial LazyFrame or a LazyFrame containing columns ['intervention', 'behavior' 'next_intervention', 'next_behavior', 'probability'].
    """
    # quick exit if there aren't 4 columns in the partial (it isn't a transition matrix)
    if len(partial.collect_schema().names()) != 4:
        return partial

    if not on_cols:
        on_cols = ["intervention", "behavior"]

    lf = _get_zero_transition_matrix(db)

    # collecting into a temporary variable so we don't materialize the partial back in the calling function
    temp = partial.collect()
    temp.columns = pl.Series(
        temp.columns).str.strip_prefix("initial_").to_list()

    parameter_cols = pl.Series(temp.columns).str.starts_with("new_").to_list()

    if sum(parameter_cols) != 1:
        raise ValueError(
            f"Invalid number of new parameters specified in DataFrame. Columns found: {parameter_cols}")
    p_col = str(temp.columns[parameter_cols.index(True)])

    left = on_cols.copy()
    right = on_cols.copy()
    if p_col.endswith("behavior"):
        left.extend(["next_behavior", "next_intervention"])
        right.extend([p_col, "intervention"])
        # expr = ((pl.col("intervention") == pl.col("next_intervention")) &
        #         (pl.col(p_col) == pl.col("next_behavior")))

    elif p_col.endswith("intervention"):
        left.extend(["next_intervention", "next_behavior"])
        right.extend([p_col, "behavior"])

        # expr = ((pl.col("behavior") == pl.col("next_behavior")) &
        #         (pl.col(p_col) == pl.col("next_intervention")))
    else:
        raise NotImplementedError(
            "Only behavior and intervention parameters are allowed to be transition matrices!")

    lf = lf.join(temp.lazy(), left_on=left, right_on=right, how="left")
    lf = lf.with_columns(
        pl.col("probability").fill_null(0.0)
    ).drop("values").select(
        ["intervention", "behavior", "next_intervention",
            "next_behavior", "probability"]
    )

    return lf


def _sort_dataframes(lf: pl.LazyFrame, db: str | Path) -> pl.LazyFrame:
    """Generalized sorting function to direct the sorting order. Only LazyFrames with state vectors (3 columns) or transition matrices (4 columns)are sorted, all other LazyFrames are returned as is.

    Args:
        lf (pl.LazyFrame): LazyFrame to sort.
        db (str | Path): A path to the database file.

    Returns:
        pl.LazyFrame: A sorted LazyFrame.
    """
    if len(lf.collect_schema().names()) == 3:
        return _sort_state_vector(lf, db)
    if len(lf.collect_schema().names()) == 4:
        return _sort_transition_matrix(lf, db)
    return lf


def _extract_values(
        p: Parameter,
        lf: pl.LazyFrame,
        *,
        n: int = 64  # 16 interventions * 4 behaviors
) -> np.ndarray:
    """Helper function to convert the dataframe rows to a numpy array reshaped into either a numpy state vector [n x 1] or transition matrix [n x n].

    Args:
        p (Parameter): The parameter we are extracting data for
        results (pl.LazyFrame): The dataframe rows
        n (int, optional): The number of states in the state vector. Defaults to 64, assuming 16 interventions and 4 behaviors.

    Raises:
        ValueError: Invalid parameter provided.

    Returns:
        np.ndarray: A numpy matrix of either [n x 1] or [n x n]
    """
    if p in [Parameter.INITIAL_COHORT, Parameter.MIGRATION_COHORT]:
        values = lf.select(pl.col("count")).collect().to_numpy().reshape(n, 1)
    elif p in [Parameter.INTERVENTION_TRANSITION_PROBABILITY,
               Parameter.BEHAVIOR_TRANSITION_PROBABILITY]:
        values = lf.select(pl.col("probability")
                           ).collect().to_numpy().reshape(n, n)
    elif p in [Parameter.OVERDOSE_PROBABILITY,
               Parameter.OVERDOSE_FATALITY_PROBABILITY]:
        values = lf.select(pl.col("probability")
                           ).collect().to_numpy().reshape(n, 1)
    elif p == Parameter.STANDARD_MORTALITY_RATIO:
        values = lf.select(pl.col("ratio")).collect().to_numpy().reshape(n, 1)
    elif p == Parameter.BACKGROUND_DEATH_PROBABILITY:
        values = np.repeat(lf.select(pl.col("probability")
                                     ).collect().to_numpy(), n).reshape(n, 1)
    else:
        raise ValueError(
            "Invalid parameter applied when attempting to extract parameters!")

    return values


def _sort_state_vector(lf: pl.LazyFrame, db: str | Path) -> pl.LazyFrame:
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
    behaviors = pl.LazyFrame(
        get_behavior_table(db), schema=["b_id", "b_name"], orient='row')

    interventions = pl.LazyFrame(
        get_intervention_table(db), schema=["i_id", "i_name"], orient='row')

    # Sort first by behaviors, then by interventions
    return lf.join(
        behaviors, left_on="behavior", right_on="b_name", how="inner"
    ).sort(pl.col("b_id")).drop("b_id").join(
        interventions, left_on="intervention", right_on="i_name", how="inner"
    ).sort(pl.col("i_id")).drop("i_id")


def _sort_transition_matrix(lf: pl.LazyFrame, db: str | Path) -> pl.LazyFrame:
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
    behaviors = pl.LazyFrame(
        get_behavior_table(db), schema=["b_id", "b_name"])

    interventions = pl.LazyFrame(
        get_intervention_table(db), schema=["i_id", "i_name"])

    # Sort order:
    #   1. Next Behavior
    #   2. Next Behavior
    #   3. Initial Behavior
    #   4. Initial Intervention
    #   e.g. [active_injection, no_treatment, active_injection, no_treatment], [active_injection, no_treatment, active_injection, buprenorphine], [active_injection, no_treatment, active_injection, methadone], etc.
    return lf.drop("i_id").join(
        behaviors, left_on="next_behavior", right_on="b_name", how="inner"
    ).sort(pl.col("b_id")).drop("b_id").join(
        interventions, left_on="next_intervention", right_on="i_name", how="inner"
    ).sort(pl.col("i_id")).drop("i_id").join(
        behaviors, left_on="behavior", right_on="b_name", how="inner"
    ).sort(pl.col("b_id")).drop("b_id").join(
        interventions, left_on="intervention", right_on="i_name", how="inner"
    ).sort(pl.col("i_id"))


def _fill_gaps_with_sample(
        partial_sample: pl.LazyFrame,
        filling_sample: pl.LazyFrame,
        *,
        value_name: str = "probability"
) -> pl.LazyFrame:
    """Helper function to fill a set of sampled parameters with fixed parameters to make a full LazyFrame.

    Args:
        partial_sample (pl.LazyFrame): The LazyFrame containing the varied parameters within a sample.
        filling_sample (pl.LazyFrame): The LazyFrame containing an entire sample (fixed and varied parameters).
        value_name (str, optional): The column name of the parameter. Defaults to "probability".

    Raises:
        ValueError: The column names do not match between the partial and filling samples.

    Returns:
        pl.LazyFrame: A LazyFrame containing both fixed and varied parameters for the sample. A state vector returns a 3 column ['intervention', 'behavior', 'value'] pattern where a transition matrix returns 4 columns ['init_intervention', 'init_behavior' 'next_parameter', 'value']. Constant values return the single column.
    """
    if partial_sample.collect_schema().names() != filling_sample.collect_schema().names():
        raise ValueError(
            f"Partially filled sample and filling sample do not have matching columns!\nPartial: {partial_sample.columns}\nFilling: {filling_sample.columns}")

    col_list = [c for c in partial_sample.collect_schema().names()
                if c != value_name]
    joined = filling_sample.join(partial_sample, on=col_list, how='left')

    joined = joined.with_columns(
        pl.when(pl.col(f"{value_name}_right").is_not_null())
        .then(pl.col(f"{value_name}_right"))
        .otherwise(pl.col(value_name)).alias("result")
    ).drop([value_name, f"{value_name}_right"]).rename(
        {"result": value_name}
    )
    return joined


def _get_zero_transition_matrix(db: str | Path) -> pl.LazyFrame:
    """Getter for setting up a fully zero transition matrix.

    Args:
        db (str | Path): File path to the database.

    Returns:
        pl.LazyFrame: A LazyFrame depicting a zero transition matrix. Columns are: ['intervention', 'behavior', 'next_intervention', 'next_behavior', 'values']
    """
    state_names = get_state_names(db)
    name_product = itertools.product(state_names, state_names)
    flat_names = [list(itertools.chain.from_iterable(t)) for t in name_product]

    try:
        lf = pl.LazyFrame(
            flat_names, orient='row',
            schema=["intervention", "behavior",
                    "next_intervention", "next_behavior"]
        ).with_columns(
            pl.lit(0.0).alias("values")
        )
    except Exception as e:
        raise e
    return lf


# External Functions


def get_data_array(
        p: Parameter,
        db: str | Path,
        sample_ids: pl.DataFrame,
        time: int | None = None
) -> np.ndarray:
    """Helper function used to extract transitions from the database based on the cohort sample and the corresponding sample IDs.

    Args:
        p (Parameter): The parameter to extract.
        db (str | Path): The string or Path object to the database.
        sample_ids (pl.DataFrame): The cohort sample containing the sample IDs.
        time (int | None): The timestep we are using to extract the transition. None is only valid when the initial cohort is being extracted.

    Raises:
        ValueError: Unimplemented Enum value.

    Returns:
        np.ndarray: The transition value as a numpy array.
    """
    time = _validate_time(time, p)
    lf = _get_parameter_data(p, db, sample_ids, time)
    lf = _fill_missing_values(lf, p, db, sample_ids, time)
    lf = _build_transition_matrix_from_partial(lf, db)
    lf = _sort_dataframes(lf, db)
    return _extract_values(p, lf, n=len(get_state_names(db)))
