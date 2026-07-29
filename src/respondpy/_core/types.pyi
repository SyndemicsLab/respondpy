################################################################################
# File: types.pyi                                                              #
# Project: respondpy                                                           #
# Created Date: 2026-07-20                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-20                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

import numpy as np
import numpy.typing as npt
import typing

StateVector = typing.Annotated[npt.NDArray[np.float64], "[m, 1]"]
TransitionMatrix = typing.Annotated[npt.NDArray[np.float64], "[m, m]"]
