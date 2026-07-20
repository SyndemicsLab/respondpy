################################################################################
# File: model.pyi                                                              #
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

from .types import StateVector
from .history import History
from .timestep import Timestep

__all__: list[str] = ['Model']


class Model:
    def __init__(self, name: str, log_name: str = "respond", log_file: str = "respond.log") -> None:
        ...

    def __copy__(self) -> Model:
        ...

    def __deepcopy__(self, arg0: dict) -> Model:
        ...

    def add_timestep(self, timestep: Timestep) -> None:
        ...

    def run_timestep(self, idx: typing.SupportsInt = -1) -> None:
        ...

    def run_timesteps(self) -> None:
        ...

    def clear_timesteps(self) -> None:
        ...

    def clear_histories(self) -> None:
        ...

    def create_default_histories(self) -> None:
        ...

    def get_timestep_at_index(self, idx: typing.SupportsInt) -> Timestep:
        ...

    def get_state(self) -> StateVector:
        ...

    def get_name(self) -> str:
        ...

    def get_histories(self) -> typing.Mapping[str, History]:
        ...

    def get_timestep(self) -> int:
        ...

    def get_history_capture_interval(self) -> typing.SupportsInt:
        ...

    def get_final_timestep(self) -> typing.SupportsInt:
        ...

    def get_initial_history_recorded(self) -> bool:
        ...

    def set_state(self, state: StateVector) -> None:
        ...

    def set_history_capture_interval(self, interval: typing.SupportsInt) -> None:
        ...

    def set_final_timestep(self, timestep: typing.SupportsInt) -> None:
        ...

    def set_initial_history_recorded(self, recorded: bool) -> None:
        ...

    def __repr__(self) -> str:
        ...
