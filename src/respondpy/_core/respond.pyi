################################################################################
# File: respond.pyi                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-08                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import typing
import collections.abc

import numpy
import numpy.typing


def migration(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Migrating Cohort.
    """


def behavior(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Behavior Transition.

    Args:
      state: The state vector
      transition: A sequence of length 1 containing the transition matrix for behavior changes.
    """


def intervention(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Intervention Transition.

    Args:
      transition: Sequence of length 2. Contains transition matrix for intervention changes and then the behavior changes once going through an intervention change.
    """


def overdose(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Overdose Transition.
    """


def mortality(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Mortality Transition.
    """
