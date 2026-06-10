################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-10                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from __future__ import annotations

from .version import version as __version__  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

from . import data

from .cost_effectiveness import (
    discount, cwise_product, cwise_min, calculate_life_years
)
from .history import History

from .model import (
    Model, build_model, add_transitions_to_model, build_model_transitions
)

from .simulation import (
    Simulation, build_simulation
)

from .transition import (
    Transition, transition_factory, build_timestep_transition
)

__all__ = [
    "data",
    "discount",
    "cwise_product",
    "cwise_min",
    "calculate_life_years",
    "History",
    "Model",
    "build_model",
    "add_transitions_to_model",
    "build_model_transitions",
    "Simulation",
    "build_simulation",
    "Transition",
    "transition_factory",
    "build_timestep_transition"
]


def __dir__() -> list[str]:
    """Return tab-completion symbols for the package namespace."""
    return __all__
