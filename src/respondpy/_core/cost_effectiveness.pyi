################################################################################
# File: cost_effectiveness.pyi                                                 #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-02                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import typing
import collections.abc

import numpy as np

from .types import CostStamp, HistoryStamp, UtilityType


def discount(data: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], discount_rate: typing.SupportsFloat, week: typing.SupportsInt, is_discrete: bool) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Calculates the Discount for the provided Vector given the discount rate, week, and flag to indicate if it is discrete or not.
    """


def discount_cost_stamp(cost_stamp: CostStamp, discount_rate: typing.SupportsFloat, week: typing.SupportsInt, is_discrete: bool) -> None:
    """
    Apply a discount to the given cost stamp.
    """


def stamp_costs(state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], healthcare_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], aod_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], fod_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], pharma_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], treatment_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]) -> CostStamp:
    """
    Build a Cost Stamp.
    """


def stamp_utilities(state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], utility: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Build a Utility Stamp.
    """


def stamp_costs_over_time(history_over_time: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], healthcare_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], aod_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], fod_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], pharma_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], treatment_costs: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], discount: bool, discount_rate: typing.SupportsFloat) -> dict[int, CostStamp]:
    """
    Stamp costs over a history time period.
    """


def stamp_utilities_over_time(history: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], utility: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], util_type: UtilityType, discount: bool, discount_rate: typing.SupportsFloat) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Stamp utilities over a history time period.
    """


def calculate_perspectives(history_over_time: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], perspectives: collections.abc.Sequence[str], healthcare_costs: collections.abc.Sequence[typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]], aod_costs: collections.abc.Sequence[typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]], fod_costs: collections.abc.Sequence[typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]], pharma_costs: collections.abc.Sequence[typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]], treatment_costs: collections.abc.Sequence[typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]], discount: bool, discount_rate: typing.SupportsFloat) -> dict[str, dict[int, CostStamp]]:
    """
    Calculate the Cost Stamps for the given perspectives.
    """


def calculate_life_years(history: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], discount: bool, discount_rate: typing.SupportsFloat) -> float:
    """
    Calculate the life years.
    """


def calculate_total_costs(costs: collections.abc.Mapping[typing.SupportsInt, CostStamp]) -> list[float]:
    """
    Calculate the total costs.
    """
