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
    """Build a simulation containing one model per cohort id.

    :param cohort_ids: Cohort identifiers to include in the simulation.
    :param input_data: Loaded input data and simulation configuration.
    :param log_name: Logger name used by the underlying core simulation/model.
    :returns: A simulation object populated with cohort-specific models.
    """
    s = Simulation(log_name)
    for cohort_id in cohort_ids:
        s.add_model(build_model(input_data, cohort_id, log_name=log_name))

    return s
