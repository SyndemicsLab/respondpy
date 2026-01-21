################################################################################
# File: parameters.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-01-15                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-15                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from enum import Enum


class Parameter(Enum):
    INITIAL_COHORT = 1
    MIGRATION_COHORT = 2
    INTERVENTION_TRANSITION_PROBABILITY = 3
    BEHAVIOR_TRANSITION_PROBABILITY = 4
    OVERDOSE_PROBABILITY = 5
    OVERDOSE_FATALITY_PROBABILITY = 6
    BACKGROUND_DEATH_PROBABILITY = 7
    STANDARD_MORTALITY_RATIO = 8
