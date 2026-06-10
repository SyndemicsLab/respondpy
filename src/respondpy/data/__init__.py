################################################################################
# File: __init__.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-06-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-10                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

from .parameters import ParameterType, Parameter

from .state_vectors import build_constant_state_vector
from .logic_conditions import (
    verify_no_nulls, verify_no_duplicates, validate_time_list
)
from .transition_matrices import (
    build_constant_transition, update_retention_probability, verify_transition_probability
)
from .input import Input

__all__ = [
    "ParameterType",
    "Parameter",
    "update_retention_probability",
    "verify_transition_probability",
    "verify_no_nulls",
    "verify_no_duplicates",
    "build_constant_transition",
    "build_constant_state_vector",
    "validate_time_list",
    "Input"
]


def __dir__() -> list[str]:
    """Return tab-completion symbols for the data namespace."""
    return __all__
