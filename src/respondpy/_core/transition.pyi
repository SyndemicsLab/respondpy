################################################################################
# File: transition.pyi                                                         #
# Project: respondpy                                                           #
# Created Date: 2026-02-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-20                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

import typing

from .history import History
from .types import StateVector, TransitionMatrix

__all__: list[str] = ['Transition']


class Transition:
    def __init__(
            self, type: str, name: str = 'transition', log_name: str = 'respond', log_file: str = 'respond.log'
    ) -> None:
        ...

    def execute(
            self,
            state: StateVector,
            history: typing.Mapping[str, History] | None = None
    ) -> tuple[StateVector, dict[str, History]]:
        ...

    def add_matrix(self, mat: TransitionMatrix) -> None:
        ...

    def get_matrices(self) -> list[TransitionMatrix]:
        ...

    def get_name(self) -> str:
        ...

    def clear_matrices(self) -> None:
        ...

    def __copy__(self) -> Transition:
        ...

    def __deepcopy__(self, arg0: dict) -> Transition:
        ...

    def __repr__(self) -> str:
        ...
