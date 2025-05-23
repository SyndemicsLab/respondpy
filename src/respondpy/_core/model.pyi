################################################################################
## File: model.pyi                                                            ##
## Project: RESPONDSimulationv2                                               ##
## Created Date: 2025-05-20                                                   ##
## Author: Matthew Carroll                                                    ##
## -----                                                                      ##
## Last Modified: 2025-05-20                                                  ##
## Modified By: Matthew Carroll                                               ##
## -----                                                                      ##
## Copyright (c) 2025 Syndemics Lab at Boston Medical Center                  ##
################################################################################

from . import data_ops

import numpy as np


def calculate_discount(data: np.ndarray, discount_rate: float,
                       N: int, discrete: bool) -> np.ndarray: ...


def calculate_costs(history: data_ops.History, cost_loader: list[data_ops.Cost],
                    perspectives: list[str], discount: bool, discount_rate: float) -> list[data_ops.Cost]: ...


def calculate_utilities(history: data_ops.History, utility_loader: list[data_ops.UtilityLoader],
                        util_type: data_ops.UtilityType, discount: bool, discount_rate: float) -> dict[int, np.ndarray]: ...


def calculate_life_years(history: data_ops.History,
                         discount: bool, discount_rate: float) -> float: ...


def calculate_total_costs(cost_list: list[data_ops.Cost]) -> list[float]: ...


class Respond:
    def __init__(self, log_name: str) -> None: ...
    def run(self, data: data_ops.DataLoader) -> None: ...
    def get_history(self) -> data_ops.History: ...
