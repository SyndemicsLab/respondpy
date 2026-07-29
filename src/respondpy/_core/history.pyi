################################################################################
# File: history.pyi                                                            #
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

__all__: list[str] = ['HistoryMode', 'get_default_history_mode', 'History']


class HistoryMode:
    """
    Members:

      kSnapshot

      kAccumulated
    """
    __members__: typing.ClassVar[
        dict[str, HistoryMode]
        # value = {'kError': <HistoryMode.kSnapshot: 0>, 'kSuccess': <HistoryMode.kAccumulated: 1>}
    ]
    # value = <HistoryMode.kSnapshot: 0>
    kSnapshot: typing.ClassVar[HistoryMode]
    # value = <HistoryMode.kAccumulated: 1>
    kAccumulated: typing.ClassVar[HistoryMode]

    def __eq__(self, other: typing.Any) -> bool:
        ...

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __ne__(self, other: typing.Any) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...


def get_default_history_mode(name: str) -> HistoryMode:
    ...


class History:
    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(
            self,
            name: str
    ) -> None:
        ...

    @typing.overload
    def __init__(self, name: str, mode: HistoryMode) -> None:
        ...

    @typing.overload
    def __init__(self, name: str, mode: HistoryMode, log_name: str) -> None:
        ...

    @typing.overload
    def __init__(self, name: str, log_name: str) -> None:
        ...

    @typing.overload
    def __init__(self, name: str, log_name: str, log_file: str) -> None:
        ...

    @typing.overload
    def __init__(
            self,
            name: str,
            mode: HistoryMode,
            log_name: str,
            log_file: str
    ) -> None:
        ...

    def __copy__(self) -> History:
        ...

    def __deepcopy__(self, arg0: dict) -> History:
        ...

    def add_state(
            self,
            state: StateVector,
            timestep: typing.SupportsInt = -1
    ) -> None:
        ...

    def accumulate_state(self, state: StateVector) -> None:
        ...

    def flush_pending_state(
        self,
        timestep: typing.SupportsInt,
        state_size: typing.SupportsInt
    ) -> None:
        ...

    def clear(self) -> None:
        ...

    def has_pending_state(self) -> bool:
        ...

    def get_state_map(self) -> typing.Mapping[int, StateVector]:
        ...

    def get_recorded_timesteps(self) -> typing.Sequence[int]:
        ...

    def get_recorded_states(self) -> typing.Sequence[StateVector]:
        ...

    def get_history_mode(self) -> HistoryMode:
        ...

    def get_pending_state(self) -> StateVector:
        ...

    def get_latest_recorded_timestep(self) -> typing.SupportsInt:
        ...

    def get_name(self) -> str:
        ...

    def get_state_as_vector(self) -> typing.Sequence[StateVector]:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

    def __repr__(self) -> str:
        ...
