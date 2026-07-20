################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-20                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from __future__ import annotations

from ._version import version as __version__  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from . import data

from .cost_effectiveness import (
    discount, cwise_product, cwise_min, calculate_life_years
)
from .history import History

from .model import Model

from .simulation import (
    Simulation, build_simulation
)

from .timestep import Timestep

from .transition import Transition

__all__ = [
    "data",
    "discount",
    "cwise_product",
    "cwise_min",
    "calculate_life_years",
    "History",
    "Model",
    "Simulation",
    "build_simulation",
    "Timestep",
    "Transition",
]


def __dir__() -> list[str]:
    """Return tab-completion symbols for the package namespace."""
    return __all__
