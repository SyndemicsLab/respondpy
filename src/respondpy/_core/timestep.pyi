################################################################################
# File: timestep.pyi                                                           #
# Project: respondpy                                                           #
# Created Date: 2026-07-20                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-20                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

import typing

from .transition import Transition
from .types import StateVector, TransitionMatrix

__all__: list[str] = ['Timestep']


class Timestep:
    def __init__(self, log_name: str, log_file: str) -> None:
        ...

    def __copy__(self) -> Timestep:
        ...

    def __deepcopy__(self, arg0: dict) -> Timestep:
        ...

    def create_transition(self, transition_name: str) -> Transition:
        ...

    def remove_transition(self, idx: typing.SupportsInt) -> Transition:
        ...

    def add_matrix_to_transition(
            self,
            idx: typing.SupportsInt | str,
            mat: StateVector | TransitionMatrix
    ) -> None:
        ...

    def get_transition(self, idx: typing.SupportsInt | str) -> Transition:
        ...

    def get_transitions(self) -> typing.Sequence[Transition]:
        ...

    def get_transition_names(self) -> typing.Sequence[str]:
        ...

    def __repr__(self) -> str:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...
