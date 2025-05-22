################################################################################
## File: utils.pyi                                                            ##
## Project: RESPONDSimulationv2                                               ##
## Created Date: 2025-05-20                                                   ##
## Author: Matthew Carroll                                                    ##
## -----                                                                      ##
## Last Modified: 2025-05-20                                                  ##
## Modified By: Matthew Carroll                                               ##
## -----                                                                      ##
## Copyright (c) 2025 Syndemics Lab at Boston Medical Center                  ##
################################################################################

from enum import Enum


class CreationStatus(Enum):
    kError = ...
    kSuccess = ...
    kExists = ...
    kNotCreated = ...


def create_file_logger(logger_name: str, file: str) -> CreationStatus: ...
