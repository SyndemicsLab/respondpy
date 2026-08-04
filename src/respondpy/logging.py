################################################################################
# File: logging.py                                                             #
# Project: respondpy                                                           #
# Created Date: 2026-08-04                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-08-04                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

from ._core.logging import (  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]
    LogType,
    CreationStatus,
    LogPattern,
    create_file_logger,
    create_shared_file_sink,
    create_shared_logger,
    set_log_pattern,
    get_log_pattern,
    set_flush_interval,
    flush_all_loggers,
    check_logger_exists,
    get_logger_info,
    set_logger_level,
    log_info,
    log_warning,
    log_error,
    log_debug,
)

__all__: list[str] = [
    "LogType",
    "CreationStatus",
    "LogPattern",
    "create_file_logger",
    "create_shared_file_sink",
    "create_shared_logger",
    "set_log_pattern",
    "get_log_pattern",
    "set_flush_interval",
    "flush_all_loggers",
    "check_logger_exists",
    "get_logger_info",
    "set_logger_level",
    "log_info",
    "log_warning",
    "log_error",
    "log_debug",
]
