################################################################################
# File: build.py                                                               #
# Project: respondpy                                                           #
# Created Date: 2026-07-23                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-29                                                    #
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
    """Build a simulation populated with one model per cohort.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    cohort_ids : Sequence of int, optional
        Cohort identifiers to include in the simulation. When omitted, all
        cohort identifiers present in ``input_data`` are used.
    log_name : str, default="respond"
        Logger name used by the underlying simulation objects.
    log_file : str, default="respond.log"
        File name used by the underlying simulation objects for logging.

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
    """Build a model for a single cohort.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    cohort_id : int
        Cohort identifier used to select the initial state and parameter
        values.
    log_name : str, default="respond"
        Logger name used by the underlying model.
    log_file : str, default="respond.log"
        File name used by the underlying model for logging.

    Returns
    -------
    Model
        A model configured with the cohort initial state and timestep
        transitions.
    """
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
                input_data.config.get(
                    "simulation", "parameter_change_times").split(),
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
    """Build a timestep containing the cohort transitions for a time point.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    cohort_id : int
        Cohort identifier used to select timestep-specific parameters.
    tstep : int, default=1
        Simulation time point represented by the timestep.
    log_name : str, default="respond"
        Logger name used by the underlying timestep.
    log_file : str, default="respond.log"
        File name used by the underlying timestep for logging.

    Returns
    -------
    Timestep
        A timestep populated with the default transitions for ``tstep``.
    """
    timestep = Timestep(log_name, log_file)

    transitions = build_default_transitions(
        input_data, cohort_id, time=tstep, log_name=log_name, log_file=log_file)

    for transition in transitions:
        timestep.add_transition(transition)

    return timestep


def build_transition(
    input_data: Input,
    cohort_id: int,
    param: Parameter,
    *,
    time: int = 1,
    log_name: str = "respond",
    log_file: str = "respond.log"
) -> Transition:
    """Build a transition for a single parameter and cohort.

    Parameters
    ----------
    input_data : Input
        Loaded input data containing the parameter matrix.
    cohort_id : int
        Cohort identifier used to select the parameter values.
    param : Parameter
        Parameter descriptor used to identify the transition and look up the
        corresponding data.
    time : int, default=1
        Time point used when selecting the parameter values.
    log_name : str, default="respond"
        Logger name used by the underlying transition.
    log_file : str, default="respond.log"
        File name used by the underlying transition for logging.

    Returns
    -------
    Transition
        A transition containing the selected parameter matrix.
    """
    transition = Transition(
        param.get_parameter_name(),
        param.get_parameter_name(),
        log_name,
        log_file
    )
    transition.add_matrix(input_data.select_parameter(param, cohort_id, time))
    return transition


def add_matrix_to_transition(
        transition: Transition,
        input_data: Input,
        cohort_id: int,
        param: Parameter,
        *,
        time: int = 1
) -> Transition:
    """Add another parameter matrix to an existing transition.

    Parameters
    ----------
    transition : Transition
        Transition to update in place.
    input_data : Input
        Loaded input data containing the parameter matrix.
    cohort_id : int
        Cohort identifier used to select the parameter values.
    param : Parameter
        Parameter descriptor used to look up the additional matrix.
    time : int, default=1
        Time point used when selecting the parameter values.

    Returns
    -------
    Transition
        The same transition instance after the matrix has been added.
    """
    transition.add_matrix(input_data.select_parameter(param, cohort_id, time))
    return transition


def build_default_transitions(
    input_data: Input,
    cohort_id: int,
    *,
    time: int = 1,
    log_name: str = "respond",
    log_file: str = "respond.log"
) -> list[Transition]:
    """Build the default transitions used by each timestep.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    cohort_id : int
        Cohort identifier used to select transition matrices.
    time : int, default=1
        Time point used when selecting parameter values.
    log_name : str, default="respond"
        Logger name used by the underlying transitions.
    log_file : str, default="respond.log"
        File name used by the underlying transitions for logging.

    Returns
    -------
    list[Transition]
        The default transition set for a timestep, in model order.
    """
    m = build_transition(
        input_data, cohort_id, Parameter(ParameterType.MIGRATION_COHORT), time=time, log_name=log_name, log_file=log_file
    )

    b = build_transition(
        input_data, cohort_id, Parameter(ParameterType.BEHAVIOR_TRANSITION_PROBABILITY), time=time, log_name=log_name, log_file=log_file
    )

    i = build_transition(
        input_data, cohort_id, Parameter(ParameterType.INTERVENTION_TRANSITION_PROBABILITY), time=time, log_name=log_name, log_file=log_file
    )

    o = build_transition(
        input_data, cohort_id, Parameter(ParameterType.OVERDOSE_PROBABILITY), time=time, log_name=log_name, log_file=log_file
    )
    o = add_matrix_to_transition(o, input_data, cohort_id, Parameter(
        ParameterType.OVERDOSE_FATALITY_PROBABILITY), time=time)

    d = build_transition(
        input_data, cohort_id, Parameter(ParameterType.BACKGROUND_DEATH_PROBABILITY), time=time, log_name=log_name, log_file=log_file
    )

    # d = add_matrix_to_transition(d, input_data, cohort_id, Parameter(
    #     ParameterType.STANDARD_MORTALITY_RATIO), time=time)

    return [m, b, i, o, d]
