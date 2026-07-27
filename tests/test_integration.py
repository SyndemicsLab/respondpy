################################################################################
# File: test_integration.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-06-29                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-16                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import sqlite3
from configparser import ConfigParser
import numpy as np
import pytest

import respondpy as rpy


@pytest.fixture
def setup_db(tmp_path_factory, db_schema, insert_complete_sample):
    """Fixture to execute before all tests to setup_db the dummy database

    Yields:
        _type_: _description_
    """
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "input.db"
    conn = sqlite3.connect(mem_str)
    cursor = conn.cursor()
    cursor.executescript(db_schema)
    cursor.executescript(insert_complete_sample)
    conn.commit()
    conn.close()
    yield mem_str


@pytest.fixture
def setup_config(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "sim.conf"
    cfg = ConfigParser()
    cfg['simulation'] = {
        'duration': '52',
        'parameter_change_times': '52',
        'stratify_entering_cohort': 'false'
    }

    cfg['output'] = {
        'build_summary_stats': 'true',
        'save_state_history': 'true',
        'timesteps_to_report': '52',
    }

    with mem_str.open('w') as configfile:
        cfg.write(configfile)

    yield mem_str


@pytest.fixture
def setup_data(setup_db, setup_config):
    """Pytest fixture to setup the data

    Args:
        setup_db (_type_): _description_
        setup_config (_type_): _description_

    Yields:
        _type_: path to database and a ConfigParser
    """
    yield setup_db, setup_config


@pytest.fixture
def setup_db_with_midrun_change(tmp_path_factory, db_schema, insert_complete_sample):
    """Build a DB with additional time-52 rows and higher migration inflow."""
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "input_104.db"
    conn = sqlite3.connect(mem_str)
    cursor = conn.cursor()
    cursor.executescript(db_schema)
    cursor.executescript(insert_complete_sample)

    # Add time-52 parameter rows. Keep all non-migration parameters identical
    # to time 1, and increase migration counts so post-52 growth is higher.
    cursor.executescript("""
INSERT INTO population_change (sample, intervention, behavior, time, count)
SELECT sample, intervention, behavior, 52, count * 3.0
FROM population_change
WHERE time = 1;

INSERT INTO intervention_transition (sample, behavior, time, initial_intervention, new_intervention, probability)
SELECT sample, behavior, 52, initial_intervention, new_intervention, probability
FROM intervention_transition
WHERE time = 1;

INSERT INTO behavior_transition (sample, intervention, time, initial_behavior, new_behavior, probability)
SELECT sample, intervention, 52, initial_behavior, new_behavior, probability
FROM behavior_transition
WHERE time = 1;

INSERT INTO smr (sample, intervention, behavior, time, ratio)
SELECT sample, intervention, behavior, 52, ratio
FROM smr
WHERE time = 1;

INSERT INTO background_mortality (sample, time, probability)
SELECT sample, 52, probability
FROM background_mortality
WHERE time = 1;

INSERT INTO overdose (sample, intervention, behavior, time, probability)
SELECT sample, intervention, behavior, 52, probability
FROM overdose
WHERE time = 1;

INSERT INTO overdose_fatality (sample, intervention, behavior, time, probability)
SELECT sample, intervention, behavior, 52, probability
FROM overdose_fatality
WHERE time = 1;
""")

    conn.commit()
    conn.close()
    yield mem_str


@pytest.fixture
def setup_db_with_flat_midrun_change(tmp_path_factory, db_schema, insert_complete_sample):
    """Build a DB with time-52 rows that match time-1 values exactly."""
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "input_104_flat.db"
    conn = sqlite3.connect(mem_str)
    cursor = conn.cursor()
    cursor.executescript(db_schema)
    cursor.executescript(insert_complete_sample)

    cursor.executescript("""
INSERT INTO population_change (sample, intervention, behavior, time, count)
SELECT sample, intervention, behavior, 52, count
FROM population_change
WHERE time = 1;

INSERT INTO intervention_transition (sample, behavior, time, initial_intervention, new_intervention, probability)
SELECT sample, behavior, 52, initial_intervention, new_intervention, probability
FROM intervention_transition
WHERE time = 1;

INSERT INTO behavior_transition (sample, intervention, time, initial_behavior, new_behavior, probability)
SELECT sample, intervention, 52, initial_behavior, new_behavior, probability
FROM behavior_transition
WHERE time = 1;

INSERT INTO smr (sample, intervention, behavior, time, ratio)
SELECT sample, intervention, behavior, 52, ratio
FROM smr
WHERE time = 1;

INSERT INTO background_mortality (sample, time, probability)
SELECT sample, 52, probability
FROM background_mortality
WHERE time = 1;

INSERT INTO overdose (sample, intervention, behavior, time, probability)
SELECT sample, intervention, behavior, 52, probability
FROM overdose
WHERE time = 1;

INSERT INTO overdose_fatality (sample, intervention, behavior, time, probability)
SELECT sample, intervention, behavior, 52, probability
FROM overdose_fatality
WHERE time = 1;
""")

    conn.commit()
    conn.close()
    yield mem_str


@pytest.fixture
def setup_config_104_change_52(tmp_path_factory):
    """Config for a 104-step run with a parameter switch at step 52."""
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "sim_104.conf"
    cfg = ConfigParser()
    cfg['simulation'] = {
        'duration': '104',
        'parameter_change_times': '52',
        'stratify_entering_cohort': 'false'
    }

    cfg['output'] = {
        'build_summary_stats': 'true',
        'save_state_history': 'true',
        'timesteps_to_report': '104',
    }

    with mem_str.open('w') as configfile:
        cfg.write(configfile)

    yield mem_str


@pytest.mark.integration
def test_simulation_run(setup_data):
    db_path, config_path = setup_data
    inp = rpy.data.Input(db_path=db_path, conf_path=config_path)
    sim = rpy.build_simulation(inp)
    sim.run()
    histories = sim.get_model_history(0)
    # state, admissions, ODs, FODs, background death
    assert len(histories) == 5
    assert len(histories['state'].get_state_map()) >= 1


@pytest.mark.integration
def test_simulation_run_104_midrun_parameter_increase(
    setup_db_with_flat_midrun_change,
    setup_db_with_midrun_change,
    setup_config_104_change_52,
):
    """Higher migration at t=52 should produce a larger final state than flat mid-run params."""
    flat_inp = rpy.data.Input(
        db_path=setup_db_with_flat_midrun_change,
        conf_path=setup_config_104_change_52,
    )
    inp = rpy.data.Input(
        db_path=setup_db_with_midrun_change,
        conf_path=setup_config_104_change_52,
    )

    flat_migration_t52 = flat_inp.select_parameter(
        rpy.data.Parameter(rpy.data.ParameterType.MIGRATION_COHORT),
        cohort_id=1,
        time=52,
    )
    flat_migration_t1 = flat_inp.select_parameter(
        rpy.data.Parameter(rpy.data.ParameterType.MIGRATION_COHORT),
        cohort_id=1,
        time=1,
    )
    assert float(np.sum(flat_migration_t52)) == float(np.sum(flat_migration_t1))

    migration_t1 = inp.select_parameter(
        rpy.data.Parameter(rpy.data.ParameterType.MIGRATION_COHORT),
        cohort_id=1,
        time=1,
    )
    migration_t52 = inp.select_parameter(
        rpy.data.Parameter(rpy.data.ParameterType.MIGRATION_COHORT),
        cohort_id=1,
        time=52,
    )
    assert float(np.sum(migration_t52)) > float(np.sum(migration_t1))

    sim_flat = rpy.build_simulation(flat_inp)
    model_flat = sim_flat.get_model(0)
    model_flat.create_default_histories()
    sim_flat.run()
    final_state_flat = model_flat.get_state()

    sim = rpy.build_simulation(inp)
    model = sim.get_model(0)
    model.create_default_histories()
    sim.run()
    final_state_changed = model.get_state()

    assert float(np.sum(final_state_changed)) > float(np.sum(final_state_flat)), (
        "Expected larger final population when migration inflow increases at "
        "timestep 52."
    )
