################################################################################
# File: simulation.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations
from collections.abc import Sequence

from .model import build_model
from .data import Input
from ._core.simulation import Simulation  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

__all__: list[str] = ['Simulation', 'build_simulation']


def build_simulation(
        cohort_ids: Sequence[int],
        input_data: Input,
        *,
        log_name: str = "console"
) -> Simulation:
    """Build a new simulation object. This function takes the cohorts, the database, and the config file then applies them to a new simulation. It creates a new model for each cohort id and adds it to the simulation returning the result.

    Args:
        cohort_ids (Sequence[int]): A sequence of ints identifying the cohorts.
        db (str | Path): A database containing the data for the simulation.
        config (ConfigParser): The `sim.conf` file used during the simulation.
        log_name (str, optional): The name of the logger to apply to the simulation. Defaults to "console".

    Returns:
        Simulation: The new simulation object.
    """
    s = Simulation(log_name)
    for cohort_id in cohort_ids:
        s.add_model(build_model(input_data, cohort_id, log_name=log_name))

    return s
