################################################################################
# File: logging.pyi                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-02-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-09-25                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations
import typing

from .config import LoggingConfig

__all__: list[str] = [
    'CreationStatus', 'LogType', 'LogPattern', 'create_file_logger',
    'configure_logger', 'create_shared_file_sink', 'create_shared_logger',
    'set_log_pattern', 'get_log_pattern', 'set_flush_interval',
    'flush_all_loggers', 'check_logger_exists', 'get_logger_info',
    'set_logger_level', 'log_info', 'log_warning', 'log_error', 'log_debug'
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


def create_file_logger(logger_name: str, filepath: str) -> CreationStatus:
    """
    Creates a File Logger for use with RESPOND.
    """


def configure_logger(config: LoggingConfig) -> CreationStatus:
    """
    Initializes a logger from a logging configuration.
    """


def create_shared_file_sink(filepath: str) -> CreationStatus:
    """
    Creates a shared file sink for use with RESPOND.
    """


def create_shared_logger(logger_name: str) -> CreationStatus:
    """
    Creates a shared logger for use with RESPOND.
    """


def set_log_pattern(pattern: LogPattern) -> None:
    """
    Sets the log pattern for all loggers.
    """


def get_log_pattern() -> LogPattern:
    """
    Gets the log pattern for all loggers.
    """


def set_flush_interval(seconds: int) -> None:
    """
    Sets the flush interval for all loggers.
    """


def flush_all_loggers() -> None:
    """
    Flushes all loggers.
    """


def check_logger_exists(logger_name: str) -> CreationStatus:
    """
    Checks if a logger exists.
    """


def get_logger_info(logger_name: str) -> str:
    """
    Gets the logger info for a logger.
    """


def set_logger_level(logger_name: str, level: int) -> None:
    """
    Sets the logger level for a logger.
    """


def log_info(logger_name: str, message: str) -> None:
    """
    Logs an info message to the log.
    """


def log_warning(logger_name: str, message: str) -> None:
    """
    Logs a warning message to the log.
    """


def log_error(logger_name: str, message: str) -> None:
    """
    Logs an error message to the log.
    """


def log_debug(logger_name: str, message: str) -> None:
    """
    Logs a debug message to the log.
    """


kDebug: LogType
kError: CreationStatus
kExists: CreationStatus
kInfo: LogType
kNotCreated: CreationStatus
kSuccess: CreationStatus
kWarn: LogType
