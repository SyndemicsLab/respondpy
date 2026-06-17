################################################################################
# File: transition.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

import numpy as np

from .data.parameters import Parameter, ParameterType
from .data.input import Input
from ._core.transition import Transition  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

__all__: list[str] = [
    'Transition', 'transition_factory', 'build_timestep_transition'
]


def transition_factory(
        name: str,
        tran_matrices: list[np.ndarray],
        *,
        log_name: str = "console"
) -> Transition:
    """Create a transition and load its ordered transition matrices.

    :param name: Transition name used by the core model.
    :param tran_matrices: Matrix/vector operands consumed in execution order.
    :param log_name: Logger name used by the underlying core transition.
    :returns: A transition ready to be attached to a model.
    """
    t = Transition(name, log_name)
    for tm in tran_matrices:
        t.add_transition_matrix(tm)
    return t


def build_timestep_transition(
        timestep: int,
        input_data: Input,
        cohort_id: int
) -> list[Transition]:
    """Build the full ordered transition set for one timestep.

    The returned transitions are: migration, intervention change, behavior
    change, overdose, and background mortality.

    :param timestep: Simulation timestep to sample.
    :param input_data: Loaded input data and simulation configuration.
    :param cohort_id: Cohort identifier used to resolve sampled parameters.
    :returns: Transition list for exactly one model timestep.
    """

    migration = transition_factory(
        "migration", [
            input_data.select_parameter(
                Parameter(ParameterType.MIGRATION_COHORT), cohort_id, timestep)
        ])

    inter = transition_factory(
        "intervention", [
            input_data.select_parameter(
                Parameter(ParameterType.INTERVENTION_TRANSITION_PROBABILITY),
                cohort_id,
                timestep
            ).T]
    )

    behav = transition_factory(
        "behavior", [
            input_data.select_parameter(
                Parameter(ParameterType.BEHAVIOR_TRANSITION_PROBABILITY),
                cohort_id,
                timestep
            ).T]
    )

    overd = transition_factory(
        "overdose", [
            input_data.select_parameter(
                Parameter(ParameterType.OVERDOSE_PROBABILITY),
                cohort_id,
                timestep
            ).squeeze(),
            input_data.select_parameter(
                Parameter(ParameterType.OVERDOSE_FATALITY_PROBABILITY),
                cohort_id,
                timestep
            ).squeeze()
        ]
    )

    morta = transition_factory(
        "background_death", [
            input_data.select_parameter(
                Parameter(ParameterType.BACKGROUND_DEATH_PROBABILITY),
                cohort_id,
                timestep
            ).squeeze() * input_data.select_parameter(
                Parameter(ParameterType.STANDARD_MORTALITY_RATIO),
                cohort_id,
                timestep
            ).squeeze()
        ]
    )

    return [migration, inter, behav, overd, morta]
