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
    if df.select(
        pl.struct(key_columns).is_duplicated().any()
    ).item():
        raise ValueError(
            f"Duplicate transition rows found for sample {sample_id} and parameter {p}"
        )


def validate_time_list(ct_list: list[int]) -> list[int]:
    """A validation function that validates and cleans up the change times from the config file.

    Args:
        ct_list (list[int]): A parsed list of integers from the `simulation.parameter_change_times` entry in the `sim.conf`

    Raises:
        ValueError: Invalid values provided in the config file.

    Returns:
        list[int]: The cleaned config values.
    """
    if any(num <= 0 for num in ct_list):
        raise ValueError(
            "The config file contains zero or a negative number in the `parameter_change_times` list!")
    ct_list.sort(reverse=True)
    if ct_list[-1] == 1:
        ct_list.pop()
    return ct_list[::-1]
