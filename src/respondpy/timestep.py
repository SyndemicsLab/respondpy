################################################################################
# File: timestep.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-07-20                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-10-13                                                    #
# Modified By: Dimitri Baptiste                                                #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

from ._core.timestep import (  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]
    Timestep,
)

__all__: list[str] = ["Timestep"]
