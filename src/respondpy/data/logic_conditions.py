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

    :param df: Data to validate.
    :param sample_id: Sample id used only for error context.
    :param p: Parameter type used only for error context.
    :param col_to_check: Column expected to be fully populated.
    :raises ValueError: If any null value is found.
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

    :param df: Data to validate.
    :param key_columns: Columns that must uniquely identify each row.
    :param sample_id: Sample id used only for error context.
    :param p: Parameter type used only for error context.
    :raises ValueError: If duplicated keys are found.
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

    :param ct_list: Parsed integer values from
        ``simulation.parameter_change_times``.
    :returns: Validated and ascending change-time list.
    :raises ValueError: If any value is less than or equal to zero.
    """
    if any(num <= 0 for num in ct_list):
        raise ValueError(
            "The config file contains zero or a negative number in the `parameter_change_times` list!")
    ct_list.sort(reverse=True)
    if ct_list[-1] == 1:
        ct_list.pop()
    return ct_list[::-1]
