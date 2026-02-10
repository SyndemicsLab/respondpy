################################################################################
# File: cost_effectiveness.pyi                                                 #
# Project: respondpy                                                           #
# Created Date: 2026-02-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-10                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

import typing
import numpy as np

from .history import History

__all__: list[str] = ['calculate_life_years',
                      'cwise_min', 'cwise_product', 'discount']


def calculate_life_years(history: History, discount: bool = False, discount_rate: typing.SupportsFloat = 0.0, total_weeks: typing.SupportsFloat = 52.0) -> float:
    """
    Calculate the life years.
    """


def cwise_min(mat1: typing.Annotated[np.typing.ArrayLike, np.float64], mat2: typing.Annotated[np.typing.ArrayLike, np.float64]) -> typing.Annotated[np.typing.ArrayLike, np.float64]:
    """
    Calculate the element wise minimum of two matrices.
    """


def cwise_product(mat1: typing.Annotated[np.typing.ArrayLike, np.float64], mat2: typing.Annotated[np.typing.ArrayLike, np.float64]) -> typing.Annotated[np.typing.ArrayLike, np.float64]:
    """
    Calculate the element wise product of two matrices.
    """


def discount(data: typing.Annotated[np.typing.ArrayLike, np.float64], discount_rate: float, week: int, is_discrete: bool = True, total_weeks: float = 52.0) -> typing.Annotated[np.typing.ArrayLike, np.float64]:
    """
    Calculates the Discount for the provided Vector given the discount rate, week, and flag to indicate if it is discrete or not.
    """
