################################################################################
# File: state_vectors.py                                                       #
# Project: respondpy                                                           #
# Created Date: 2026-06-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-17                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import polars as pl


def build_constant_state_vector(
    interventions: list,
    behaviors: list,
    *,
    sample_id: int = 1,
    time: int = 1,
    value_column: str = "count",
    constant: float = 0.0
) -> pl.DataFrame:
    """Build a fully populated constant-valued state vector table.

    Parameters
    ----------
    interventions : list
        Ordered intervention names.
    behaviors : list
        Ordered behavior names.
    sample_id : int, default=1
        Sample identifier written into output rows.
    time : int, default=1
        Timestep written into output rows.
    value_column : str, default="count"
        Name of the generated value column.
    constant : float, default=0.0
        Constant value assigned to every state row.

    Returns
    -------
    polars.DataFrame
        Cross-product dataframe with one row per intervention-behavior state.
    """
    inter = pl.DataFrame({"intervention": interventions})

    behav = pl.DataFrame({"behavior": behaviors})

    df = inter.join(
        behav, how="cross"
    ).with_columns(
        pl.lit(sample_id).alias("sample"),
        pl.lit(time).alias("time"),
        pl.lit(constant).alias(value_column)
    ).select(["sample", "intervention", "behavior", "time", value_column])

    return df
