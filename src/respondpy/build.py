################################################################################
# File: build.py                                                               #
# Project: respondpy                                                           #
# Created Date: 2026-07-23                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-11-12                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser, NoOptionError, NoSectionError
from os import cpu_count

from .data import Input, Parameter, ParameterType, validate_time_list
from .config import LoggingConfig, RuntimeConfig
from .simulation import Simulation
from .model import Model
from .timestep import Timestep
from .transition import Transition


def _get_simulation_settings(input_data: Input) -> tuple[int, list[int]]:
    """Read and validate required simulation settings from an Input source."""
    config: ConfigParser = input_data.config
    try:
        duration = config.getint("simulation", "duration")
    except (NoOptionError, NoSectionError, ValueError) as error:
        raise ValueError(
            "The simulation config requires a positive integer "
            "`simulation.duration`."
        ) from error
    if duration <= 0:
        raise ValueError(
            "The simulation config requires a positive `duration`."
        )

    try:
        raw_change_times = config.get("simulation", "parameter_change_times")
        change_times = [int(value) for value in raw_change_times.split()]
    except (NoOptionError, NoSectionError, ValueError) as error:
        raise ValueError(
            "The simulation config requires integer "
            "`simulation.parameter_change_times` values."
        ) from error
    return duration, validate_time_list(change_times)


def _build_model_chunk(
    input_data: Input,
    cohort_ids: Sequence[int],
    processor_count: int | None,
    log_name: str,
    log_file: str,
) -> list[Model]:
    """Build a Model Chunk to give to a worker.

    This is a helper function for parallel building. A worker is assigned a chunk of models to build. This construncts that chunk.

    Parameters
    ----------
    input_data : Input
        The Input data that is used with the models.
    cohort_ids : Sequence[int]
        The list of cohorts that correspond to each model.
    processor_count : int | None
        The number of processors to give to each model during simulation.
    log_name : str
        The name of the logger
    log_file : str
        The log file path

    Returns
    -------
    list[Model]
        A list of built models for a worker.
    """
    with input_data._new_worker_input() as worker_input:
        return [
            build_model(
                worker_input,
                cohort_id,
                processor_count=processor_count,
                log_name=log_name,
                log_file=log_file,
            )
            for cohort_id in cohort_ids
        ]


def build_simulation(
    input_data: Input,
    *,
    processor_count: int | None = None,
    cohort_ids: Sequence[int] | None = None,
    log_name: str = "respond",
    log_file: str = "respond.log",
    build_workers: int = 1,
    build_min_parallel_cohorts: int = 8,
    build_chunk_size: int = 2,
    build_waves_per_worker: int = 2
) -> Simulation:
    """Build a simulation populated with one model per cohort.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    processor_count: int, optional
        The number of processors (threads) to use when a model runs. When
        omitted, the maximum number of available processors is used.
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
    runtime_config = RuntimeConfig()
    runtime_config.logging.logger_name = log_name
    runtime_config.logging.file_path = log_file
    if processor_count:
        runtime_config.execution.total_threads = processor_count
    s = Simulation(runtime_config)
    duration, _ = _get_simulation_settings(input_data)
    s.set_duration(duration)

    cohort_ids = tuple(cohort_ids)
    worker_count = min(build_workers, cpu_count() or 1)

    # Note: We turn off Pylint below because `isinstance(input_data, Input)`
    # allows for parallelism for Input subclasses. While we don't have
    # subclasses to Input, we don't want to allow any future subclasses to be
    # parallel by default and thus force check Input as a parallel-path guard
    if (
        worker_count > 1
        and type(input_data) is Input  # pylint: disable=unidiomatic-typecheck
        and len(cohort_ids) >= build_min_parallel_cohorts
    ):
        for n, v in (
            ("build_chunk_size", build_chunk_size),
            ("build_waves_per_worker", build_waves_per_worker),
        ):
            if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
                raise ValueError(f"{n} must be a positive integer")
        wave_size = worker_count * build_chunk_size * build_waves_per_worker
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            for start in range(0, len(cohort_ids), wave_size):
                wave_ids = cohort_ids[start: start + wave_size]
                chunks = [
                    wave_ids[index: index + build_chunk_size]
                    for index in range(0, len(wave_ids), build_chunk_size)
                ]
                futures = [
                    executor.submit(
                        _build_model_chunk,
                        input_data,
                        chunk,
                        processor_count,
                        log_name,
                        log_file,
                    )
                    for chunk in chunks
                ]
                try:
                    model_chunks = [future.result() for future in futures]
                except BaseException:
                    for future in futures:
                        future.cancel()
                    raise

                for model_chunk in model_chunks:
                    for model in model_chunk:
                        s.add_model(model)
                del model_chunks, futures
    else:
        for cohort_id in cohort_ids:
            s.add_model(
                build_model(
                    input_data,
                    cohort_id,
                    processor_count=processor_count,
                    log_name=log_name,
                    log_file=log_file,
                )
            )

    return s


def build_model(
    input_data: Input,
    cohort_id: int,
    *,
    processor_count: int | None = None,
    log_name: str = "respond",
    log_file: str = "respond.log",
) -> Model:
    """Build a model for a single cohort.

    Parameters
    ----------
    input_data : Input
        Loaded input data and simulation configuration.
    cohort_id : int
        Cohort identifier used to select the initial state and parameter
        values.
    processor_count : int, optional
        The number of processors (threads) to use when a model runs. When
        omitted, the maximum number of available processors is used.
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
    # if the number of threads to use is specified, use the correct model
    # constructor
    if processor_count:
        runtime_config = RuntimeConfig()
        runtime_config.execution.total_threads = processor_count
        runtime_config.logging.logger_name = log_name
        runtime_config.logging.file_path = log_file
        model = Model("markov", runtime_config)
    else:
        runtime_config = RuntimeConfig()
        runtime_config.logging.logger_name = log_name
        runtime_config.logging.file_path = log_file
        model = Model("markov", runtime_config)

    initial_state = input_data.select_parameter(
        Parameter(ParameterType.INITIAL_COHORT),
        cohort_id,
    )
    model.set_state(initial_state)

    duration, change_times = _get_simulation_settings(input_data)
    schedule_times = [1, *change_times]
    timestep_cache: dict[int, Timestep] = {}

    for model_timestep in range(1, duration + 1):
        parameter_time = max(t for t in schedule_times if t <= model_timestep)
        if parameter_time not in timestep_cache:
            timestep_cache[parameter_time] = build_timestep(
                input_data,
                cohort_id,
                parameter_time,
                log_name=log_name,
                log_file=log_file,
            )
        model.add_timestep(timestep_cache[parameter_time])
    return model


def build_timestep(
    input_data: Input,
    cohort_id: int,
    tstep: int = 1,
    *,
    log_name: str = "respond",
    log_file: str = "respond.log",
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
    logging_config = LoggingConfig()
    logging_config.logger_name = log_name
    logging_config.file_path = log_file
    timestep = Timestep(logging_config)

    transitions = build_default_transitions(
        input_data, cohort_id, time=tstep, log_name=log_name, log_file=log_file
    )

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
    log_file: str = "respond.log",
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
    logging_config = LoggingConfig()
    logging_config.logger_name = log_name
    logging_config.file_path = log_file
    transition = Transition(
        param.get_parameter_name(), param.get_parameter_name(), logging_config
    )
    transition.add_matrix(input_data.select_parameter(param, cohort_id, time))
    return transition


def add_matrix_to_transition(
    transition: Transition,
    input_data: Input,
    cohort_id: int,
    param: Parameter,
    *,
    time: int = 1,
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
    log_file: str = "respond.log",
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
        input_data,
        cohort_id,
        Parameter(ParameterType.MIGRATION_COHORT),
        time=time,
        log_name=log_name,
        log_file=log_file,
    )

    b = build_transition(
        input_data,
        cohort_id,
        Parameter(ParameterType.BEHAVIOR_TRANSITION_PROBABILITY),
        time=time,
        log_name=log_name,
        log_file=log_file,
    )

    i = build_transition(
        input_data,
        cohort_id,
        Parameter(ParameterType.INTERVENTION_TRANSITION_PROBABILITY),
        time=time,
        log_name=log_name,
        log_file=log_file,
    )

    o = build_transition(
        input_data,
        cohort_id,
        Parameter(ParameterType.OVERDOSE_PROBABILITY),
        time=time,
        log_name=log_name,
        log_file=log_file,
    )
    o = add_matrix_to_transition(
        o,
        input_data,
        cohort_id,
        Parameter(ParameterType.OVERDOSE_FATALITY_PROBABILITY),
        time=time,
    )

    d = build_transition(
        input_data,
        cohort_id,
        Parameter(ParameterType.BACKGROUND_DEATH_PROBABILITY),
        time=time,
        log_name=log_name,
        log_file=log_file,
    )

    d.get_matrices()[0] = d.get_matrices()[0] * input_data.select_parameter(
        Parameter(ParameterType.STANDARD_MORTALITY_RATIO), cohort_id, time=time
    )

    return [m, b, i, o, d]
