################################################################################
# File: simulation.pyi                                                         #
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

from .model import Model
from .history import History

__all__: list[str] = ['Simulation']


class Simulation:
    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, log_name: str) -> None:
        ...

    @typing.overload
    def __init__(self, log_name: str, log_file: str) -> None:
        ...

    def __copy__(self) -> Simulation:
        ...

    def __deepcopy__(self, arg0: dict) -> Simulation:
        ...

    def create_new_model(self, model_name: str) -> str:
        ...

    def clear_models(self) -> None:
        ...

    def add_model(self, model: Model) -> None:
        ...

    def run(self, duration: typing.SupportsInt = -1) -> None:
        ...

    def get_models(self) -> list[Model]:
        ...

    @typing.overload
    def get_model(self, idx: typing.SupportsInt) -> Model:
        ...

    @typing.overload
    def get_model(self, model_name: str) -> Model:
        ...

    def get_model_names(self) -> list[str]:
        ...

    @typing.overload
    def get_model_history(self, idx: typing.SupportsInt) -> typing.Mapping[str, History]:
        ...

    @typing.overload
    def get_model_history(self, model_name: str) -> typing.Mapping[str, History]:
        ...

    @typing.overload
    def get_model_history_names(self, idx: typing.SupportsInt) -> list[str]:
        ...

    @typing.overload
    def get_model_history_names(self, model_name: str) -> list[str]:
        ...

    def set_duration(self, duration: typing.SupportsInt) -> None:
        ...
