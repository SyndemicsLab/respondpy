################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-28                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from __future__ import annotations

from ._version import version as __version__  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from . import data
from . import logging

from .cost_effectiveness import (
    discount, cwise_product, cwise_min, calculate_life_years
)
from .history import History
from .model import Model
from .simulation import Simulation
from .timestep import Timestep
from .transition import Transition

from .build import build_simulation, build_model, build_timestep, build_default_transitions, build_transition, add_matrix_to_transition


__all__ = [
    "data",
    "logging",
    "discount",
    "cwise_product",
    "cwise_min",
    "calculate_life_years",
    "History",
    "Model",
    "Simulation",
    "Timestep",
    "Transition",
    "build_simulation",
    "build_model",
    "build_timestep",
    "build_default_transitions",
    "build_transition",
    "add_matrix_to_transition"
]


def __dir__() -> list[str]:
    """Return tab-completion symbols for the package namespace."""
    return __all__
