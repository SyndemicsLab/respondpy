################################################################################
# File: transition.pyi                                                         #
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
import collections.abc

import numpy
import numpy.typing
import respondpy._core.history
import typing

__all__: list[str] = ['Transition']


class Transition:
    def __copy__(self) -> Transition:
        ...

    def __deepcopy__(self, arg0: dict) -> Transition:
        """
        memo
        """

    def __init__(self, type: str, log_name: str = 'console') -> None:
        ...

    def __repr__(self) -> str:
        ...

    def add_transition_matrix(self, mat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...

    def clear_transition_matrices(self) -> None:
        ...

    def execute(self, state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], history: collections.abc.Mapping[str, respondpy._core.history.History]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...

    def get_log_name(self) -> str:
        ...

    def get_transition_name(self) -> str:
        ...
