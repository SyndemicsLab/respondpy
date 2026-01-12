################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-12                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from __future__ import annotations

import typing
import collections.abc

import numpy
import numpy.typing

from respondpy.sqlite_eigen import (
    get_init_cohort_from_db, get_population_change_from_db, get_intervention_transitions_from_db, get_behavior_transitions_from_db, get_overdose_from_db, get_fatal_overdose_from_db, get_background_mortality_from_db, get_smr_from_db
)

from ._core.cost_effectiveness import (  # pylint: disable=import-error,no-name-in-module
    discount, discount_cost_stamp, stamp_costs, stamp_utilities, stamp_costs_over_time, stamp_utilities_over_time, calculate_perspectives, calculate_life_years, calculate_total_costs
)

from ._core.logging import (  # pylint: disable=import-error,no-name-in-module
    LogType, CreationStatus, create_file_logger, log_info, log_warning, log_error, log_debug, kDebug, kError, kExists, kInfo, kNotCreated, kSuccess, kWarn
)

from ._core.markov import Markov  # pylint: disable=import-error,no-name-in-module


from ._core.respond import (  # pylint: disable=import-error,no-name-in-module
    migration, behavior, intervention, overdose, mortality
)


from ._core.types import (  # pylint: disable=import-error,no-name-in-module
    HistoryStamp, CostStamp, UtilityType, ResultSets, Totals, kMin, kMult
)

# pylint: disable-next=import-error
from .version import version as __version__

vector_1d: typing.TypeAlias = typing.Annotated[numpy.typing.ArrayLike,
                                               numpy.float64, "[m, 1]"]

vector_of_matrices: typing.TypeAlias = collections.abc.Sequence[
    typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]

transition_function: typing.TypeAlias = typing.Callable[[vector_1d,
                                                         vector_of_matrices], vector_1d]

transition: typing.TypeAlias = tuple[transition_function, vector_of_matrices]

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
