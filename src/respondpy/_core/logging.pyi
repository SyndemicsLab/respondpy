################################################################################
# File: logging.pyi                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-02-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-08-04                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations
import typing

__all__: list[str] = [
    'CreationStatus', 'LogType', 'create_file_logger', 'kDebug', 'kError',
    'kExists', 'kInfo', 'kNotCreated', 'kSuccess', 'kWarn', 'log_debug',
    'log_error', 'log_info', 'log_warning'
]


class LogType:
    """
    Members:

      kInfo

      kWarn

      kError

      kDebug
    """
    __members__: typing.ClassVar[dict[str, LogType]
                                 # value = {'kInfo': <LogType.kInfo: 0>, 'kWarn': <LogType.kWarn: 1>, 'kError': <LogType.kError: 2>, 'kDebug': <LogType.kDebug: 3>}
                                 ]
    kDebug: typing.ClassVar[LogType]  # value = <LogType.kDebug: 3>
    kError: typing.ClassVar[LogType]  # value = <LogType.kError: 2>
    kInfo: typing.ClassVar[LogType]  # value = <LogType.kInfo: 0>
    kWarn: typing.ClassVar[LogType]  # value = <LogType.kWarn: 1>

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


class CreationStatus:
    """
    Members:

      kError

      kSuccess

      kExists

      kNotCreated
    """
    __members__: typing.ClassVar[
        dict[str, CreationStatus]
        # value = {'kError': <CreationStatus.kError: -1>, 'kSuccess': <CreationStatus.kSuccess: 0>, 'kExists': <CreationStatus.kExists: 1>, 'kNotCreated': <CreationStatus.kNotCreated: 2>}
    ]
    # value = <CreationStatus.kError: -1>
    kError: typing.ClassVar[CreationStatus]
    # value = <CreationStatus.kSuccess: 0>
    kSuccess: typing.ClassVar[CreationStatus]
    # value = <CreationStatus.kExists: 1>
    kExists: typing.ClassVar[CreationStatus]
    # value = <CreationStatus.kNotCreated: 2>
    kNotCreated: typing.ClassVar[CreationStatus]

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


class LogPattern:
    """
    Members:

      kSimple

      kStandard

      kDetailed

      kThreadSafe
    """
    __members__: typing.ClassVar[
        dict[str, LogPattern]
        # value = {'kSimple': <LogPattern.kSimple: 0>, 'kStandard': <LogPattern.kStandard: 1>, 'kDetailed': <LogPattern.kDetailed: 2>, 'kThreadSafe': <LogPattern.kThreadSafe: 3>}
    ]
    # value = <LogPattern.kSimple: 0>
    kSimple: typing.ClassVar[LogPattern]
    # value = <LogPattern.kStandard: 1>
    kStandard: typing.ClassVar[LogPattern]
    # value = <LogPattern.kDetailed: 2>
    kDetailed: typing.ClassVar[LogPattern]
    # value = <LogPattern.kThreadSafe: 3>
    kThreadSafe: typing.ClassVar[LogPattern]

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


def create_file_logger(arg0: str, arg1: str) -> CreationStatus:
    """
    Creates a File Logger for use with RESPOND.
    """


def create_shared_file_sink(arg0: str) -> CreationStatus:
    """
    Creates a shared file sink for use with RESPOND.
    """


def create_shared_logger(arg0: str, arg1: str) -> CreationStatus:
    """
    Creates a shared logger for use with RESPOND.
    """


def set_log_pattern(arg0: LogPattern) -> None:
    """
    Sets the log pattern for all loggers.
    """


def get_log_pattern() -> LogPattern:
    """
    Gets the log pattern for all loggers.
    """


def set_flush_interval(arg0: int) -> None:
    """
    Sets the flush interval for all loggers.
    """


def flush_all_loggers() -> None:
    """
    Flushes all loggers.
    """


def check_logger_exists(arg0: str) -> bool:
    """
    Checks if a logger exists.
    """


def get_logger_info(arg0: str) -> tuple[LogType, str]:
    """
    Gets the logger info for a logger.
    """


def set_logger_level(arg0: str, arg1: LogType) -> None:
    """
    Sets the logger level for a logger.
    """


def log_info(arg0: str, arg1: str) -> None:
    """
    Logs an info message to the log.
    """


def log_warning(arg0: str, arg1: str) -> None:
    """
    Logs a warning message to the log.
    """


def log_error(arg0: str, arg1: str) -> None:
    """
    Logs an error message to the log.
    """


def log_debug(arg0: str, arg1: str) -> None:
    """
    Logs a debug message to the log.
    """


kDebug: LogType  # value = <LogType.kDebug: 3>
kError: CreationStatus  # value = <CreationStatus.kError: -1>
kExists: CreationStatus  # value = <CreationStatus.kExists: 1>
kInfo: LogType  # value = <LogType.kInfo: 0>
kNotCreated: CreationStatus  # value = <CreationStatus.kNotCreated: 2>
kSuccess: CreationStatus  # value = <CreationStatus.kSuccess: 0>
kWarn: LogType  # value = <LogType.kWarn: 1>
