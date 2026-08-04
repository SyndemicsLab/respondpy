################################################################################
# File: test_integration.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2026-06-29                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-08-04                                                    #
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
        'duration': '1',
        'parameter_change_times': '1',
        'stratify_entering_cohort': 'false'
    }

    cfg['output'] = {
        'build_summary_stats': 'true',
        'save_state_history': 'true',
        'timesteps_to_report': '1',
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
    assert float(np.sum(flat_migration_t52)) == float(
        np.sum(flat_migration_t1))

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


@pytest.fixture
def setup_db_for_numerical_check(tmp_path_factory, db_schema):
    """Build deterministic dummy data for math-focused integration checks."""
    temp_dir = tmp_path_factory.mktemp("test-data")
    db_path = temp_dir / "input_numerical.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(db_schema)
    cursor.executescript("""
INSERT INTO cohort (id, description, background_mortality_sample, behavior_transition_sample, initial_population_sample, intervention_transition_sample, overdose_sample, overdose_fatality_sample, population_change_sample, smr_sample)
VALUES (1, "Numerical Cohort", 1, 1, 1, 1, 1, 1, 1, 1);

INSERT INTO intervention (id, name)
VALUES (1, "i1"), (2, "i2");

INSERT INTO behavior (id, name)
VALUES (1, "b1"), (2, "b2");

INSERT INTO initial_population (sample, intervention, behavior, count)
VALUES
    (1, 1, 1, 100.0),
    (1, 1, 2, 80.0),
    (1, 2, 1, 60.0),
    (1, 2, 2, 40.0);

INSERT INTO population_change (sample, intervention, behavior, time, count)
VALUES
    (1, 1, 1, 1, 1.0),
    (1, 1, 2, 1, -2.0),
    (1, 2, 1, 1, 3.0),
    (1, 2, 2, 1, -1.0);

INSERT INTO behavior_transition (sample, intervention, time, initial_behavior, new_behavior, probability)
VALUES
    (1, 1, 1, 1, 1, 0.9),
    (1, 1, 1, 1, 2, 0.1),
    (1, 1, 1, 2, 1, 0.2),
    (1, 1, 1, 2, 2, 0.8),
    (1, 2, 1, 1, 1, 0.85),
    (1, 2, 1, 1, 2, 0.15),
    (1, 2, 1, 2, 1, 0.25),
    (1, 2, 1, 2, 2, 0.75);

INSERT INTO intervention_transition (sample, behavior, time, initial_intervention, new_intervention, probability)
VALUES
    (1, 1, 1, 1, 1, 0.95),
    (1, 1, 1, 1, 2, 0.05),
    (1, 1, 1, 2, 1, 0.10),
    (1, 1, 1, 2, 2, 0.90),
    (1, 2, 1, 1, 1, 0.92),
    (1, 2, 1, 1, 2, 0.08),
    (1, 2, 1, 2, 1, 0.15),
    (1, 2, 1, 2, 2, 0.85);

INSERT INTO overdose (sample, intervention, behavior, time, probability)
VALUES
    (1, 1, 1, 1, 0.05),
    (1, 1, 2, 1, 0.04),
    (1, 2, 1, 1, 0.03),
    (1, 2, 2, 1, 0.02);

INSERT INTO overdose_fatality (sample, intervention, behavior, time, probability)
VALUES
    (1, 1, 1, 1, 0.20),
    (1, 1, 2, 1, 0.10),
    (1, 2, 1, 1, 0.15),
    (1, 2, 2, 1, 0.25);

INSERT INTO background_mortality (sample, time, probability)
VALUES (1, 1, 0.01);

INSERT INTO smr (sample, intervention, behavior, time, ratio)
VALUES
    (1, 1, 1, 1, 1.2),
    (1, 1, 2, 1, 1.0),
    (1, 2, 1, 1, 1.1),
    (1, 2, 2, 1, 0.9);
""")
    conn.commit()
    conn.close()

    yield db_path


@pytest.fixture
def setup_config_one_executed_timestep(tmp_path_factory):
    """Config for exactly one executed timestep.

    RESPOND records timestep 0 as the initial state, so duration 1 runs one
    transition step.
    """
    temp_dir = tmp_path_factory.mktemp("test-data")
    config_path = temp_dir / "sim_one_step.conf"
    cfg = ConfigParser()
    cfg['simulation'] = {
        'duration': '1',
        'parameter_change_times': '1',
        'stratify_entering_cohort': 'false',
    }
    cfg['output'] = {
        'build_summary_stats': 'true',
        'save_state_history': 'true',
        'timesteps_to_report': '1',
    }

    with config_path.open('w') as configfile:
        cfg.write(configfile)

    yield config_path


@pytest.fixture
def setup_config_fifty_two_executed_timesteps(tmp_path_factory):
    """Config for exactly fifty-two executed timesteps.

    RESPOND records timestep 0 as the initial state, so duration 52 runs
    fifty-two transition steps.
    """
    temp_dir = tmp_path_factory.mktemp("test-data")
    config_path = temp_dir / "sim_52_steps.conf"
    cfg = ConfigParser()
    cfg['simulation'] = {
        'duration': '52',
        'parameter_change_times': '1',
        'stratify_entering_cohort': 'false',
    }
    cfg['output'] = {
        'build_summary_stats': 'true',
        'save_state_history': 'true',
        'timesteps_to_report': '52',
    }

    with config_path.open('w') as configfile:
        cfg.write(configfile)

    yield config_path


@pytest.mark.integration
def test_single_timestep_numerical_state_matches_expected(
    setup_db_for_numerical_check,
    setup_config_one_executed_timestep,
):
    """Single-step run should match manually computed transition math."""
    inp = rpy.data.Input(
        db_path=setup_db_for_numerical_check,
        conf_path=setup_config_one_executed_timestep,
    )
    sim = rpy.build_simulation(inp)
    sim.run()

    final_state = sim.get_model(0).get_state()
    expected_state = np.array(
        [105.36565049999999, 71.49283020000001, 61.394525775000005, 38.11650975]
    )

    np.testing.assert_allclose(
        final_state, expected_state, rtol=1e-10, atol=1e-10)


@pytest.mark.integration
def test_fifty_two_timestep_numerical_state_matches_expected(
    setup_db_for_numerical_check,
    setup_config_fifty_two_executed_timesteps,
):
    """Fifty-two-step run should match manually computed transition math."""
    inp = rpy.data.Input(
        db_path=setup_db_for_numerical_check,
        conf_path=setup_config_fifty_two_executed_timesteps,
    )
    sim = rpy.build_simulation(inp)
    sim.run()

    final_state = sim.get_model(0).get_state()
    expected_state = np.array(
        [63.99771165143241, 28.195217933852412,
            39.53089805842006, 19.00629313025105]
    )

    np.testing.assert_allclose(
        final_state, expected_state, rtol=1e-9, atol=1e-9)


@pytest.mark.integration
def test_behavior_and_intervention_matrices_are_column_stochastic(setup_data):
    """Behavior and intervention matrices should be column-stochastic for y=Mx."""
    db_path, config_path = setup_data
    inp = rpy.data.Input(db_path=db_path, conf_path=config_path)
    sim = rpy.build_simulation(inp)

    timestep = sim[0].get_timestep_at_index(0)
    transition_names = timestep.get_transition_names()

    behavior_matrix = timestep[
        transition_names.index("behavior")
    ].get_matrices()[0]
    intervention_matrix = timestep[
        transition_names.index("intervention")
    ].get_matrices()[0]

    np.testing.assert_allclose(
        behavior_matrix.sum(axis=0),
        np.ones(behavior_matrix.shape[1]),
        atol=1e-12,
        rtol=0.0,
    )
    np.testing.assert_allclose(
        intervention_matrix.sum(axis=0),
        np.ones(intervention_matrix.shape[1]),
        atol=1e-12,
        rtol=0.0,
    )


@pytest.mark.integration
def test_behavior_then_intervention_preserves_mass_one_step(setup_data):
    """Applying behavior then intervention should preserve total mass."""
    db_path, config_path = setup_data
    inp = rpy.data.Input(db_path=db_path, conf_path=config_path)
    sim = rpy.build_simulation(inp)

    model = sim[0]
    x0 = model.get_state()

    timestep = model.get_timestep_at_index(0)
    transition_names = timestep.get_transition_names()
    behavior_matrix = timestep[
        transition_names.index("behavior")
    ].get_matrices()[0]
    intervention_matrix = timestep[
        transition_names.index("intervention")
    ].get_matrices()[0]

    x1 = behavior_matrix @ x0
    x2 = intervention_matrix @ x1

    np.testing.assert_allclose(
        float(np.sum(x1)), float(np.sum(x0)), atol=1e-12, rtol=0.0
    )
    np.testing.assert_allclose(
        float(np.sum(x2)), float(np.sum(x1)), atol=1e-12, rtol=0.0
    )


@pytest.mark.integration
def test_transition_matrix_indices_match_state_name_order(setup_data):
    """Matrix indices should map as M[destination_state, source_state]."""
    db_path, config_path = setup_data
    inp = rpy.data.Input(db_path=db_path, conf_path=config_path)

    state_names = inp.get_state_names()
    state_to_idx = {state: idx for idx, state in enumerate(state_names)}

    for param_type in (
        rpy.data.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY,
        rpy.data.ParameterType.INTERVENTION_TRANSITION_PROBABILITY,
    ):
        param = rpy.data.Parameter(param_type)
        matrix = inp.select_parameter(param, cohort_id=1, time=1)

        sample_id = inp._get_sample_id_for_parameter(param, cohort_id=1)
        long_df = inp._get_parameter_filled(
            param, sample_id=sample_id, time=1).collect()

        for row in long_df.iter_rows(named=True):
            src = (row["initial_intervention"], row["initial_behavior"])
            dst = (row["new_intervention"], row["new_behavior"])
            src_idx = state_to_idx[src]
            dst_idx = state_to_idx[dst]

            np.testing.assert_allclose(
                matrix[dst_idx, src_idx],
                row["probability"],
                atol=1e-12,
                rtol=0.0,
            )
