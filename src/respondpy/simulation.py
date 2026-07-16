################################################################################
# File: simulation.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-11                                                    #
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
        input_data: Input,
        *,
        cohort_ids: Sequence[int] | None = None,
        log_name: str = "console"
) -> Simulation:
    """Build a simulation containing one model per cohort id.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    cohort_ids : Sequence of int, optional
        Cohort identifiers to include in the simulation.
    log_name : str, default="console"
        Logger name used by the underlying core simulation/model.

    Returns
    -------
    Simulation
        A simulation object populated with cohort-specific models.

    Raises
    ------
    ValueError
        If any requested cohort id is not present in ``input_data``.
    """
    input_cohort_ids = input_data.get_cohort_ids()
    if cohort_ids is None:
        cohort_ids = input_cohort_ids
    else:
        missing_cohorts = set(cohort_ids) - set(input_cohort_ids)
        if missing_cohorts:
            raise ValueError(
                f"Cohort IDs {missing_cohorts} not found in input data."
            )
    s = Simulation(log_name)
    for cohort_id in cohort_ids:
        s.add_model(build_model(input_data, cohort_id, log_name=log_name))

    return s
