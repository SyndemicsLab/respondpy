################################################################################
# File: transition.pyi                                                         #
# Project: respondpy                                                           #
# Created Date: 2026-02-02                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-02                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import typing
import collections.abc

import numpy as np

from .types import HistoryStamp


class Transition:
    """
    Helper class describing the Transition requirements.
    """

    def __init__(self) -> None:
        ...

    def SetCallback(
            self,
            callback: typing.Callable[[
                typing.Annotated[
                    np.typing.ArrayLike, np.float64, "[m, 1]"
                ], collections.abc.Sequence[
                    typing.Annotated[
                        np.typing.ArrayLike, np.float64, "[m, 1]"]
                ], HistoryStamp
            ],
            typing.Annotated[
                np.typing.ArrayLike,
                np.float64, "[m, 1]"
            ]]
    ) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
        """
        Setter for the callback function
        """

    def Execute(self, state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], ts: collections.abc.Sequence[typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]], hs: HistoryStamp) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
        """
        Execution function for running the callback
        """
