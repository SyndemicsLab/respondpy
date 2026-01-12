################################################################################
# File: cost_effectiveness.pyi                                                 #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-08                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import typing
import collections.abc

from .types import CostStamp, HistoryStamp, UtilityType, vector_1d


def discount(data: vector_1d, discount_rate: typing.SupportsFloat, week: typing.SupportsInt, is_discrete: bool) -> vector_1d:
    """
    Calculates the Discount for the provided Vector given the discount rate, week, and flag to indicate if it is discrete or not.
    """


def discount_cost_stamp(cost_stamp: CostStamp, discount_rate: typing.SupportsFloat, week: typing.SupportsInt, is_discrete: bool) -> None:
    """
    Apply a discount to the given cost stamp.
    """


def stamp_costs(state: vector_1d, healthcare_costs: vector_1d, aod_costs: vector_1d, fod_costs: vector_1d, pharma_costs: vector_1d, treatment_costs: vector_1d) -> CostStamp:
    """
    Build a Cost Stamp.
    """


def stamp_utilities(state: vector_1d, utility: vector_1d) -> vector_1d:
    """
    Build a Utility Stamp.
    """


def stamp_costs_over_time(history_over_time: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], healthcare_costs: vector_1d, aod_costs: vector_1d, fod_costs: vector_1d, pharma_costs: vector_1d, treatment_costs: vector_1d, discount: bool, discount_rate: typing.SupportsFloat) -> dict[int, CostStamp]:
    """
    Stamp costs over a history time period.
    """


def stamp_utilities_over_time(history: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], utility: vector_1d, util_type: UtilityType, discount: bool, discount_rate: typing.SupportsFloat) -> vector_1d:
    """
    Stamp utilities over a history time period.
    """


def calculate_perspectives(history_over_time: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], perspectives: collections.abc.Sequence[str], healthcare_costs: collections.abc.Sequence[vector_1d], aod_costs: collections.abc.Sequence[vector_1d], fod_costs: collections.abc.Sequence[vector_1d], pharma_costs: collections.abc.Sequence[vector_1d], treatment_costs: collections.abc.Sequence[vector_1d], discount: bool, discount_rate: typing.SupportsFloat) -> dict[str, dict[int, CostStamp]]:
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
