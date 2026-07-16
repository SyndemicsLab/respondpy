################################################################################
# File: logic_conditions.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-06-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl

from respondpy.data.parameters import ParameterType


def verify_no_nulls(
        df: pl.DataFrame,
        sample_id: int,
        p: ParameterType,
        *,
        col_to_check: str = "probability"
) -> None:
    """Validate that a required value column contains no null values.

    Parameters
    ----------
    df : polars.DataFrame
        Data to validate.
    sample_id : int
        Sample id used only for error context.
    p : ParameterType
        Parameter type used only for error context.
    col_to_check : str, default="probability"
        Column expected to be fully populated.

    Raises
    ------
    ValueError
        If any null value is found.
    """
    if df.select(pl.col(col_to_check).is_null().any()).item():
        raise ValueError(
            f"Null transition probabilities found for sample {sample_id} and parameter {p}"
        )


def verify_no_duplicates(
        df: pl.DataFrame,
        key_columns: list[str],
        sample_id: int,
        p: ParameterType
) -> None:
    """Validate that key columns uniquely identify transition rows.

    Parameters
    ----------
    df : polars.DataFrame
        Data to validate.
    key_columns : list of str
        Columns that must uniquely identify each row.
    sample_id : int
        Sample id used only for error context.
    p : ParameterType
        Parameter type used only for error context.

    Raises
    ------
    ValueError
        If duplicated keys are found.
    """
    if df.select(
        pl.struct(key_columns).is_duplicated().any()
    ).item():
        raise ValueError(
            f"Duplicate transition rows found for sample {sample_id} and parameter {p}"
        )


def validate_time_list(ct_list: list[int]) -> list[int]:
    """Validate and normalize configured parameter change times.

    The value ``1`` is removed because timestep 1 is always explicitly built in
    model construction.

    Parameters
    ----------
    ct_list : list of int
        Parsed integer values from ``simulation.parameter_change_times``.

    Returns
    -------
    list of int
        Validated and ascending change-time list.

    Raises
    ------
    ValueError
        If any value is less than or equal to zero.
    """
    if any(num <= 0 for num in ct_list):
        raise ValueError(
            "The config file contains zero or a negative number in the `parameter_change_times` list!")
    ct_list.sort(reverse=True)
    if ct_list[-1] == 1:
        ct_list.pop()
    return ct_list[::-1]
