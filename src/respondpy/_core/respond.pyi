################################################################################
# File: respond.pyi                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
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


def migration(
        state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"],
        transitions: collections.abc.Sequence[typing.Annotated[
            np.typing.ArrayLike, np.float64, "[m, n]"]],
        stamp: HistoryStamp
) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Applies the Migrating Cohort.
    """


def behavior(
        state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[
            np.typing.ArrayLike, np.float64, "[m, n]"]],
        history: HistoryStamp
) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Applies the Behavior Transition.

    Args:
      state: The state vector
      transition: A sequence of length 1 containing the transition matrix for behavior changes.
      history: A HistoryStamp variable to record any changes.
    """


def intervention(
        state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[
            np.typing.ArrayLike, np.float64, "[m, n]"]],
        history: HistoryStamp
) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Applies the Intervention Transition.

    Args:
      transition: Sequence of length 2. Contains transition matrix for intervention changes and then the behavior changes once going through an intervention change.
      history: A HistoryStamp variable to record any changes.
    """


def overdose(
        state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[
            np.typing.ArrayLike, np.float64, "[m, n]"]],
        history: HistoryStamp
) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Applies the Overdose Transition.
    """


def mortality(
        state: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[
            np.typing.ArrayLike, np.float64, "[m, n]"]],
        history: HistoryStamp
) -> typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]:
    """
    Applies the Mortality Transition.
    """
