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
    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, log_name: str) -> None:
        ...

    @typing.overload
    def __init__(self, log_name: str, log_file: str) -> None:
        ...

    def __copy__(self) -> Timestep:
        ...

    def __deepcopy__(self, arg0: dict) -> Timestep:
        ...

    def create_transition(self, transition_name: str) -> Transition:
        ...

    def add_transition(self, transition: Transition) -> None:
        ...

    def remove_transition(self, idx: typing.SupportsInt) -> Transition:
        ...

    @typing.overload
    def add_matrix_to_transition(
        self,
        idx: typing.SupportsInt,
        mat: StateVector | TransitionMatrix
    ) -> None:
        ...

    @typing.overload
    def add_matrix_to_transition(
        self,
        transition_name: str,
        mat: StateVector | TransitionMatrix
    ) -> None:
        ...

    @typing.overload
    def get_transition(self, idx: typing.SupportsInt) -> Transition:
        ...

    @typing.overload
    def get_transition(self, transition_name: str) -> Transition:
        ...

    def get_transitions(self) -> typing.Sequence[Transition]:
        ...

    def get_transition_names(self) -> typing.Sequence[str]:
        ...

    def __getitem__(self, idx: typing.SupportsInt) -> Transition:
        ...

    def __setitem__(self, idx: typing.SupportsInt, transition: Transition) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...
