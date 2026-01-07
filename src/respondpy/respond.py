################################################################################
# File: respond.py                                                             #
# Project: respondpy                                                           #
# Created Date: 2026-01-07                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-07                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################
from __future__ import annotations
from typing import TYPE_CHECKING

import sys

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

try:
    from . import respondpy
except ImportError as err:
    if "respondpy" not in str(err):
        raise
    new_msg = "Did you compile the RESPOND C++ extension module? Use CMake or scikit-build-core to build."
    if sys.version_info >= (3, 11):
        err.add_note(new_msg)
        raise
    total_msg = f"{err}\n{new_msg}"
    new_exception = type(err)(new_msg, name=err.name, path=err.path)
    raise new_exception from err

if TYPE_CHECKING:
    from respondpy.respondpy import CostStamp, CreationStatus, HistoryStamp, LogType, Markov, ResultSets, Totals, UtilityType, behavior, calculate_life_years, calculate_perspectives, calculate_total_costs, create_file_logger, discount, discount_cost_stamp, intervention, kDebug, kError, kExists, kInfo, kMin, kMult, kNotCreated, kSuccess, kWarn, log_debug, log_error, log_info, log_warning, migration, mortality, overdose, stamp_costs, stamp_costs_over_time, stamp_utilities, stamp_utilities_over_time
else:
    CostStamp = Any
    CreationStatus = Any
    HistoryStamp = Any
    LogType = Any
    Markov = Any
    ResultSets = Any
    Totals = Any
    UtilityType = Any
    behavior = Any
    calculate_life_years = Any
    calculate_perspectives = Any
    calculate_total_costs = Any
    create_file_logger = Any
    discount = Any
    discount_cost_stamp = Any
    intervention = Any
    kDebug = Any
    kError = Any
    kExists = Any
    kInfo = Any
    kMin = Any
    kMult = Any
    kNotCreated = Any
    kSuccess = Any
    kWarn = Any
    log_debug = Any
    log_error = Any
    log_info = Any
    log_warning = Any
    migration = Any
    mortality = Any
    overdose = Any
    stamp_costs = Any
    stamp_costs_over_time = Any
    stamp_utilities = Any
    stamp_utilities_over_time = Any

__all__ = (
    "CostStamp",
    "CreationStatus",
    "HistoryStamp",
    "LogType",
    "Markov",
    "ResultSets",
    "Totals",
    "UtilityType",
    "behavior",
    "calculate_life_years",
    "calculate_perspectives",
    "calculate_total_costs",
    "create_file_logger",
    "discount",
    "discount_cost_stamp",
    "intervention",
    "kDebug",
    "kError",
    "kExists",
    "kInfo",
    "kMin",
    "kMult",
    "kNotCreated",
    "kSuccess",
    "kWarn",
    "log_debug",
    "log_error",
    "log_info",
    "log_warning",
    "migration",
    "mortality",
    "overdose",
    "stamp_costs",
    "stamp_costs_over_time",
    "stamp_utilities",
    "stamp_utilities_over_time"
)
