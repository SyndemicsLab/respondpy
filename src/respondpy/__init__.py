################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-07                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from __future__ import annotations

from respondpy.sqlite_eigen import (
    get_init_cohort_from_db, get_population_change_from_db, get_intervention_transitions_from_db, get_behavior_transitions_from_db, get_overdose_from_db, get_fatal_overdose_from_db, get_background_mortality_from_db, get_smr_from_db
)

from respondpy.respond import *  # noqa: F401

__all__ = [
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
    "stamp_utilities_over_time",
    "get_init_cohort_from_db",
    "get_population_change_from_db",
    "get_intervention_transitions_from_db",
    "get_behavior_transitions_from_db",
    "get_overdose_from_db",
    "get_fatal_overdose_from_db",
    "get_background_mortality_from_db",
    "get_smr_from_db"
]


def __dir__() -> list[str]:
    return __all__
