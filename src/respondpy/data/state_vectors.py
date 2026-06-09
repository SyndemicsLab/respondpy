################################################################################
# File: state_vectors.py                                                       #
# Project: respondpy                                                           #
# Created Date: 2026-06-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-08                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl


def build_constant_state_vector(
    num_interventions: int,
    num_behaviors: int,
    *,
    sample_id: int = 1,
    time: int = 1,
    value_column: str = "probability",
    constant: float = 0.0
) -> pl.DataFrame:
    """Helper function to build a zero state vector. This is used when we have no sampled values for a state vector and need to fill in the zeros.

    Args:
        sample (int): The sample ID for the row of the cohort table we are filling in.
        interventions (list[str]): The list of interventions in the model.
        behaviors (list[str]): The list of behaviors in the model.

    Returns:
        pl.LazyFrame: A LazyFrame containing all combinations of interventions and behaviors with a value of 0.0. Columns are ['intervention', 'behavior', 'value'].
    """
    interventions = pl.DataFrame(
        {"intervention": pl.arange(0, num_interventions, eager=True)})

    behaviors = pl.DataFrame(
        {"behavior": pl.arange(0, num_behaviors, eager=True)})

    df = interventions.join(
        behaviors, how="cross"
    ).with_columns(
        pl.lit(sample_id).alias("sample"),
        pl.lit(time).alias("time"),
        pl.lit(constant).alias(value_column)
    ).select(["sample", "intervention", "behavior", "time", value_column])

    return df
