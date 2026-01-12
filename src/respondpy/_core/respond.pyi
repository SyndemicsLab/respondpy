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

from .types import vector_1d, vector_of_matrices


def migration(
        state: vector_1d,
        transition: vector_of_matrices) -> vector_1d:
    """
    Applies the Migrating Cohort.
    """


def behavior(state: vector_1d, transition: vector_of_matrices) -> vector_1d:
    """
    Applies the Behavior Transition.

    Args:
      state: The state vector
      transition: A sequence of length 1 containing the transition matrix for behavior changes.
    """


def intervention(state: vector_1d, transition: vector_of_matrices) -> vector_1d:
    """
    Applies the Intervention Transition.

    Args:
      transition: Sequence of length 2. Contains transition matrix for intervention changes and then the behavior changes once going through an intervention change.
    """


def overdose(state: vector_1d, transition: vector_of_matrices) -> vector_1d:
    """
    Applies the Overdose Transition.
    """


def mortality(state: vector_1d, transition: vector_of_matrices) -> vector_1d:
    """
    Applies the Mortality Transition.
    """
