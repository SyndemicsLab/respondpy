################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-03                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from __future__ import annotations
from .version import version as __version__  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from .data.parameters import Parameter
from .data.transition_matrices import (
    update_retention_probability,
    verify_transition_probability,
)

from .execute.build_simulation import build_simulation
from .execute.build_transition import get_data_array

from .io.reading import (
    get_parameter_by_id_and_time, get_state_names, get_behaviors, get_interventions, get_cohorts, get_behavior_table, get_intervention_table, get_sample_ids_by_table
)
from .io.writing import insert_parameter, insert_cohort

from ._core.cost_effectiveness import discount, cwise_product, cwise_min, calculate_life_years  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from ._core.history import History  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from ._core.logging import CreationStatus, LogType, create_file_logger, kDebug, kError, kExists, kInfo, kNotCreated, kSuccess, kWarn, log_debug, log_error, log_info, log_warning   # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from ._core.model import Model  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from ._core.simulation import Simulation  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from ._core.transition import Transition  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

__all__ = [
    "Parameter",  # data.parameters
    "update_retention_probability",
    "verify_transition_probability",
    "build_simulation",
    "get_data_array",
    "get_parameter_by_id_and_time",  # io.reading
    "get_state_names",
    "get_behaviors",
    "get_interventions",
    "get_behavior_table",
    "get_intervention_table",
    "get_cohorts",
    "get_sample_ids_by_table",
    "insert_parameter",  # io.writing
    "insert_cohort",
    "discount",  # _core.cost_effectiveness
    "cwise_product",
    "cwise_min",
    "calculate_life_years",
    "History",  # _core.history
    "CreationStatus",  # _core.logging
    "kError",
    "kExists",
    "kNotCreated",
    "kSuccess",
    "LogType",
    "kInfo",
    "kWarn",
    "kDebug",
    "create_file_logger",
    "log_debug",
    "log_error",
    "log_info",
    "log_warning",
    "Model",  # _core.model
    "Simulation",  # _core.simulation
    "Transition"  # _core.transition
]


def __dir__() -> list[str]:
    return __all__
