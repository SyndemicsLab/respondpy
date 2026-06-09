################################################################################
# File: model.py                                                               #
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
    m = Model(name, log_name)
    init_pop = input_data.select_parameter(
        Parameter(ParameterType.INITIAL_COHORT), cohort_id, time=1, raw=True).squeeze()
    m.set_state(init_pop)
    m = build_model_transitions(m, input_data, cohort_id)
    return m


def build_model_transitions(
        model: Model,
        input_data: Input,
        cohort_id: int
) -> Model:
    """Helper function to build the transition list for the Markov model.

    Args:
        model (Model): The model we are intended to add transitions to.
        db (str | Path): The string or Path object to the database file.
        config (ConfigParser): The object containing the config data.
        sample_ids (pl.DataFrame): The cohort sample containing all the sample ids.

    Returns:
        rpy.Markov: The Markov model with the transitions added for the entire duration.
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
    """Helper function to add the transitions to the Markov model.

    Args:
        model (Model): The model to add the transitions to.
        t_transition (list[Transition]): A timestep (i.e. a list of transitions)

    Returns:
        rpy.Markov: The Markov model with the transitions added.
    """
    for t in t_transition:
        model.add_transition(t)
    return model
