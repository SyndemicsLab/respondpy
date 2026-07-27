################################################################################
# File: build.py                                                               #
# Project: respondpy                                                           #
# Created Date: 2026-07-23                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-27                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

from collections.abc import Sequence

from .data import Input, Parameter, ParameterType, validate_time_list
from .simulation import Simulation
from .model import Model
from .timestep import Timestep
from .transition import Transition


def build_simulation(
        input_data: Input,
        *,
        cohort_ids: Sequence[int] | None = None,
        log_name: str = "respond",
        log_file: str = "respond.log"
) -> Simulation:
    """Build a simulation containing one model per cohort id.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    cohort_ids : Sequence of int, optional
        Cohort identifiers to include in the simulation.
    log_name : str, default="console"
        Logger name used by the underlying core simulation/model.

    Returns
    -------
    Simulation
        A simulation object populated with cohort-specific models.

    Raises
    ------
    ValueError
        If any requested cohort id is not present in ``input_data``.
    """
    input_cohort_ids = input_data.get_cohort_ids()
    if cohort_ids is None:
        cohort_ids = input_cohort_ids
    else:
        missing_cohorts = set(cohort_ids) - set(input_cohort_ids)
        if missing_cohorts:
            raise ValueError(
                f"Cohort IDs {missing_cohorts} not found in input data."
            )
    s = Simulation(log_name, log_file)
    duration = int(input_data.config.get("simulation", "duration"))
    s.set_duration(duration)
    for cohort_id in cohort_ids:
        s.add_model(build_model(input_data, cohort_id))

    return s


def build_model(
    input_data: Input,
    cohort_id: int,
    *,
    log_name: str = "respond",
    log_file: str = "respond.log"
) -> Model:
    model = Model("markov", log_name, log_file)
    initial_state = input_data.select_parameter(
        Parameter(ParameterType.INITIAL_COHORT),
        cohort_id,
    )
    model.set_state(initial_state)

    change_times = validate_time_list(
        list(
            map(
                int,
                input_data.config.get("simulation", "parameter_change_times").split(),
            )
        )
    )

    duration = int(input_data.config.get("simulation", "duration"))
    schedule_times = [1, *change_times]

    for model_timestep in range(1, duration):
        parameter_time = max(t for t in schedule_times if t <= model_timestep)
        model.add_timestep(build_timestep(
            input_data,
            cohort_id,
            parameter_time,
            log_name=log_name,
            log_file=log_file,
        ))
    return model


def build_timestep(
    input_data: Input,
    cohort_id: int,
    tstep: int = 1,
    *,
    log_name: str = "respond",
    log_file: str = "respond.log"
) -> Timestep:
    timestep = Timestep(log_name, log_file)

    transitions = build_default_transitions(
        input_data, cohort_id, time=tstep, log_name=log_name, log_file=log_file)

    for transition in transitions:
        timestep.add_transition(transition)

    return timestep


def build_default_transitions(
    input_data: Input,
    cohort_id: int,
    *,
    time: int = 1,
    log_name: str = "respond",
    log_file: str = "respond.log"
) -> list[Transition]:
    m = Transition("migration", "migration", log_name, log_file)
    m.add_matrix(input_data.select_parameter(
        Parameter(ParameterType.MIGRATION_COHORT), cohort_id, time))
    b = Transition("behavior", "behavior", log_name, log_file)
    b.add_matrix(input_data.select_parameter(
        Parameter(ParameterType.BEHAVIOR_TRANSITION_PROBABILITY), cohort_id, time))
    i = Transition("intervention", "intervention", log_name, log_file)
    i.add_matrix(input_data.select_parameter(
        Parameter(ParameterType.INTERVENTION_TRANSITION_PROBABILITY), cohort_id, time))
    o = Transition("overdose", "overdose", log_name, log_file)
    o.add_matrix(input_data.select_parameter(
        Parameter(ParameterType.OVERDOSE_PROBABILITY), cohort_id, time))
    o.add_matrix(input_data.select_parameter(
        Parameter(ParameterType.OVERDOSE_FATALITY_PROBABILITY), cohort_id, time))
    d = Transition("background_death", "background_death", log_name, log_file)
    d.add_matrix(input_data.select_parameter(
        Parameter(ParameterType.BACKGROUND_DEATH_PROBABILITY), cohort_id, time))

    return [m, b, i, o, d]
