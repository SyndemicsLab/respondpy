################################################################################
# File: simulation.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-10-13                                                    #
# Modified By: Dimitri Baptiste                                                #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

from ._core.simulation import (  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]
    Simulation,
)

__all__: list[str] = ["Simulation"]
