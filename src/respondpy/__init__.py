################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-26                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from __future__ import annotations
from .version import version as __version__  # pylint: disable=import-error,no-name-in-module

from .data.parameters import Parameter

from .execute.build_simulation import build_simulation
from .execute.build_transition import get_data_array

from .io.reading import (
    get_parameter_by_id_and_time, get_state_names, get_behaviors, get_interventions, get_cohorts, get_behavior_table, get_intervention_table, get_sample_ids_by_table
)
from .io.writing import insert_parameter, insert_cohort

from ._core.cost_effectiveness import discount, cwise_product, cwise_min, calculate_life_years  # pylint: disable=import-error,no-name-in-module

from ._core.history import History, HistoryMode, Snapshot, Accumulated, get_default_history_mode  # pylint: disable=import-error,no-name-in-module

from ._core.logging import CreationStatus, kError, kExists, kNotCreated, kSuccess, LogType, kInfo, kWarn, kDebug, LogPattern, kSimple, kStandard, kDetailed, kThreadSafe, create_file_logger, create_shared_file_sink, create_shared_logger, set_log_pattern, get_log_pattern, set_flush_interval, flush_all_loggers, check_logger_exists, get_logger_info, set_logger_level, log_debug, log_error, log_info, log_warning  # pylint: disable=import-error,no-name-in-module

from ._core.model import Model  # pylint: disable=import-error,no-name-in-module

from ._core.simulation import Simulation  # pylint: disable=import-error,no-name-in-module

from ._core.transition import Transition  # pylint: disable=import-error,no-name-in-module

__all__ = [
    "Parameter",  # data.parameters
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
    "HistoryMode",
    "Snapshot",
    "Accumulated",
    "get_default_history_mode",
    "CreationStatus",  # _core.logging
    "kError",
    "kExists",
    "kNotCreated",
    "kSuccess",
    "LogType",
    "kInfo",
    "kWarn",
    "kDebug",
    "LogPattern",
    "kSimple",
    "kStandard",
    "kDetailed",
    "kThreadSafe",
    "create_file_logger",
    "create_shared_file_sink",
    "create_shared_logger",
    "set_log_pattern",
    "get_log_pattern",
    "set_flush_interval",
    "flush_all_loggers",
    "check_logger_exists",
    "get_logger_info",
    "set_logger_level",
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
