################################################################################
# File: model.pyi                                                              #
# Project: respondpy                                                           #
# Created Date: 2026-02-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-25                                                    #
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

from .transition import Transition

__all__: list[str] = ['Model']


class Model:
    def __copy__(self) -> Model:
        ...

    def __deepcopy__(self, arg0: dict) -> Model:
        """
        memo
        """

    def __init__(self, name: str, log_name: str = 'console') -> None:
        ...

    def __repr__(self) -> str:
        ...

    def add_transition(self, transition: Transition) -> None:
        ...

    def clear_transitions(self) -> None:
        ...

    def get_histories(self) -> dict[str, respondpy._core.history.History]:
        ...

    def get_log_name(self) -> str:
        ...

    def get_model_name(self) -> str:
        ...

    def get_state(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...

    def get_transition_names(self) -> list[str]:
        ...

    def run_transitions(self) -> None:
        ...

    def set_histories(self, histories: collections.abc.Mapping[str, respondpy._core.history.History]) -> None:
        ...

    def set_state(self, state: numpy.typing.NDArray[numpy.float64]) -> None:
        ...

    def create_default_histories(self) -> None:
        ...
