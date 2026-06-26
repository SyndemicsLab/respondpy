################################################################################
# File: model.py                                                               #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-25                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################
from __future__ import annotations

from .data.input import Input
from .data.logic_conditions import validate_time_list
from .data.parameters import Parameter, ParameterType
from .transition import Transition, build_timestep_transition
from ._core.model import Model  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]
from ._utils import str_to_int_list

__all__: list[str] = [
    'Model', 'build_model',
    'add_transitions_to_model', 'build_model_transitions'
]


def build_model(
        input_data: Input,
        cohort_id: int = 1,
        *,
        name: str = "markov",
        log_name: str = "console"
) -> Model:
    """Build a Model with initialized state and configured transitions.

    :param input_data: Loaded input data and simulation configuration.
    :param cohort_id: Cohort identifier used to resolve sampled parameters.
    :param name: Model name passed to the core model constructor.
    :param log_name: Logger name used by the underlying core model.
    :returns: A model ready to be added to a simulation.
    """
    m = Model(name, log_name)
    init_pop = input_data.select_parameter(
        Parameter(ParameterType.INITIAL_COHORT), cohort_id, time=1)
    m.set_state(init_pop)
    m = build_model_transitions(m, input_data, cohort_id)
    return m


def build_model_transitions(
        model: Model,
        input_data: Input,
        cohort_id: int
) -> Model:
    """Populate a model with per-timestep transitions for full duration.

    The first transition block is built from timestep 1. Additional timestep
    transition blocks are either copied or rebuilt at configured
    ``parameter_change_times`` values.

    :param model: Model instance to mutate.
    :param input_data: Loaded input data and simulation configuration.
    :param cohort_id: Cohort identifier used to resolve sampled parameters.
    :returns: The same model instance, with transitions appended.
    """
    # Add the first timestep
    ct_val = 1
    transition = build_timestep_transition(ct_val, input_data, cohort_id)
    add_transitions_to_model(model, transition)
    duration = input_data.config.getint('simulation', 'duration')
    change_times = validate_time_list(
        str_to_int_list(input_data.config.get(
            'simulation', 'parameter_change_times'))
    )

    # we start at 2 because 0 is in the initial state, 1 is the first transition (added above), and now we look for more transitions. If there is no other change times then we just make copies.
    for i in range(1, duration):
        if change_times and i == change_times[-1]:
            ct_val = change_times.pop()
            transition = build_timestep_transition(
                ct_val, input_data, cohort_id)
            add_transitions_to_model(model, transition)
        else:
            add_transitions_to_model(model, transition.copy())
    return model


def add_transitions_to_model(
        model: Model,
        t_transition: list[Transition]
) -> Model:
    """Append one timestep's transitions to a model.

    :param model: Model to update.
    :param t_transition: Transition objects for one simulation timestep.
    :returns: The same model instance, for chaining.
    """
    for t in t_transition:
        model.add_transition(t)
    return model
