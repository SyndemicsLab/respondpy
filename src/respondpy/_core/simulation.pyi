################################################################################
# File: simulation.pyi                                                         #
# Project: respondpy                                                           #
# Created Date: 2026-02-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-12                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

from collections.abc import Sequence

import numpy
import numpy.typing
import respondpy._core.history
import respondpy._core.model
import typing

__all__: list[str] = ['Simulation']


class Simulation:
    def __copy__(self) -> Simulation:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, log_name: str) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def add_model(self, model: respondpy._core.model.Model) -> None:
        ...

    def clear_models(self) -> None:
        ...

    def get_log_name(self) -> str:
        ...

    def get_model_histories(self) -> Sequence[dict[str, list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]]]:
        ...

    def get_model_history_names(self) -> list[tuple[str, str]]:
        ...

    def get_model_names(self) -> list[str]:
        ...

    def get_models(self) -> list[respondpy._core.model.Model]:
        ...

    def run(self) -> None:
        ...
