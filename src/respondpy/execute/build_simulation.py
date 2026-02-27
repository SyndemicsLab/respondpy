################################################################################
# File: build_simulation.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-02-26                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-26                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from pathlib import Path
from configparser import ConfigParser
from collections.abc import Sequence

import polars as pl
import numpy as np

from respondpy._core.transition import Transition  # pylint: disable=import-error,no-name-in-module
from respondpy._core.model import Model  # pylint: disable=import-error,no-name-in-module
from respondpy._core.simulation import Simulation  # pylint: disable=import-error,no-name-in-module
from respondpy.data.parameters import Parameter
from respondpy.io.reading import get_cohorts
from respondpy.execute.build_transition import get_data_array


def _get_list_of_ints(config_string: str) -> list[int]:
    """Converts a comma-separated string into a list of integers

    Args:
        config_string (str): A comma-separated string

    Returns:
        list[int]: The list of integers from the string
    """
    return [int(x.strip()) for x in config_string.split(',')]


def _build_single_transition(name: str, tran_matrices: list[np.ndarray], *, log_name: str = "console") -> Transition:
    t = Transition(name, log_name)
    for tm in tran_matrices:
        t.add_transition_matrix(tm)
    return t


def _build_timestep(
        timestep: int,
        db: str | Path,
        sample_ids: pl.DataFrame
) -> list[Transition]:
    """Helper function to build a single timestep because a timestep consists of the same transitions.

    Args:
        timestep (int): The integer for the timestep we want to build.
        db (str | Path): The location of the database file.
        sample_ids (pl.DataFrame): The cohort with the sample ids.

    Returns:
        list[Transition]: The list of transitions that make the timestep.
    """

    migration = _build_single_transition("migration", [
        get_data_array(Parameter.MIGRATION_COHORT,
                       db, sample_ids, timestep).squeeze()
    ])

    inter = _build_single_transition("intervention", [
        get_data_array(
            Parameter.INTERVENTION_TRANSITION_PROBABILITY, db, sample_ids, timestep
        ).T
    ])

    behav = _build_single_transition("behavior", [
        get_data_array(
            Parameter.BEHAVIOR_TRANSITION_PROBABILITY, db, sample_ids, timestep
        ).T
    ])

    overd = _build_single_transition("overdose", [
        get_data_array(
            Parameter.OVERDOSE_PROBABILITY, db, sample_ids, timestep
        ).squeeze(),
        get_data_array(
            Parameter.OVERDOSE_FATALITY_PROBABILITY, db, sample_ids, timestep
        ).squeeze()
    ])

    morta = _build_single_transition("background_death", [
        get_data_array(
            Parameter.STANDARD_MORTALITY_RATIO, db, sample_ids, timestep
        ).squeeze() * get_data_array(
            Parameter.BACKGROUND_DEATH_PROBABILITY, db, sample_ids, timestep
        ).squeeze()
    ])

    return [migration, inter, behav, overd, morta]


def _add_transitions(
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


def _valid_change_times(ct_list: list[int]) -> list[int]:
    """A validation function that validates and cleans up the change times from the config file.

    Args:
        ct_list (list[int]): A parsed list of integers from the `simulation.parameter_change_times` entry in the `sim.conf`

    Raises:
        ValueError: Invalid values provided in the config file.

    Returns:
        list[int]: The cleaned config values.
    """
    if any(num <= 0 for num in ct_list):
        raise ValueError(
            "The config file contains zero or a negative number in the `parameter_change_times` list!")
    ct_list.sort(reverse=True)
    if ct_list[-1] == 1:
        ct_list.pop()
    return ct_list


def _build_transitions(
        model: Model,
        db: str | Path,
        config: ConfigParser,
        sample_ids: pl.DataFrame
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
    transition = _build_timestep(ct_val, db, sample_ids)
    _add_transitions(model, transition)
    duration = config.getint('simulation', 'duration')
    change_times = _valid_change_times(
        _get_list_of_ints(config.get('simulation', 'parameter_change_times'))
    )

    # we start at 2 because 0 is in the initial state, 1 is the first transition (added above), and now we look for more transitions. If there is no other change times then we just make copies.
    for i in range(1, duration):
        if change_times and i == change_times[-1]:
            ct_val = change_times.pop()
            transition = _build_timestep(ct_val, db, sample_ids)
            _add_transitions(model, transition)
        else:
            _add_transitions(model, transition.copy())
    return model


def _build_new_model(
        db: str | Path,
        config: ConfigParser,
        sample_ids: pl.DataFrame,
        *,
        name: str = "markov",
        log_name: str = "console"
) -> Model:
    m = Model(name, log_name)
    init_pop = get_data_array(
        Parameter.INITIAL_COHORT, db, sample_ids).squeeze()
    m.set_state(init_pop)
    m = _build_transitions(m, db, config, sample_ids)
    return m


def build_simulation(
        cohort_ids: Sequence[int],
        db: str | Path,
        config: ConfigParser,
        *,
        log_name: str = "console"
) -> Simulation:
    """Build a new simulation object. This function takes the cohorts, the database, and the config file then applies them to a new simulation. It creates a new model for each cohort id and adds it to the simulation returning the result.

    Args:
        cohort_ids (Sequence[int]): A sequence of ints identifying the cohorts.
        db (str | Path): A database containing the data for the simulation.
        config (ConfigParser): The `sim.conf` file used during the simulation.
        log_name (str, optional): The name of the logger to apply to the simulation. Defaults to "console".

    Returns:
        Simulation: The new simulation object.
    """
    s = Simulation(log_name)
    col_names, cohorts = get_cohorts(db)
    for cohort_id in cohort_ids:
        sample_ids = pl.DataFrame(
            cohorts, schema=col_names, orient='row'
        ).filter(pl.col("id") == cohort_id)
        s.add_model(_build_new_model(
            db, config, sample_ids, log_name=log_name
        ))

    return s
