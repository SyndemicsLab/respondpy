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
    """_summary_

    Args:
        name (str): _description_
        tran_matrices (list[np.ndarray]): _description_
        log_name (str, optional): _description_. Defaults to "console".

    Returns:
        Transition: _description_
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
    """Helper function to build a single timestep because a timestep consists of the same transitions.

    Args:
        timestep (int): The integer for the timestep we want to build.
        db (str | Path): The location of the database file.
        sample_ids (pl.DataFrame): The cohort with the sample ids.

    Returns:
        list[Transition]: The list of transitions that make the timestep.
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
