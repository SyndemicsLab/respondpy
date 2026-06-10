################################################################################
# File: test_data_input.py                                                     #
# Project: respondpy                                                           #
# Created Date: 2026-06-10                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-10                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import sqlite3
from configparser import ConfigParser
from pathlib import Path

import pytest
import numpy as np

import respondpy.data as rpydata


@pytest.fixture
def make_tempdir(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test-data")
    yield temp_dir


@pytest.fixture
def setup_db(make_tempdir, db_schema, insert_complete_sample):
    """Fixture to execute before all tests to setup_db the dummy database

    Yields:
        _type_: _description_
    """
    temp_dir = make_tempdir
    mem_str = temp_dir / "input.db"
    conn = sqlite3.connect(mem_str)
    cursor = conn.cursor()
    cursor.executescript(db_schema)
    cursor.executescript(insert_complete_sample)
    conn.commit()
    conn.close()
    yield mem_str


@pytest.fixture
def setup_config(make_tempdir):
    temp_dir = make_tempdir
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


@pytest.mark.unit
def test_input_initialization(setup_data):
    db_path, config_path = setup_data
    input_data = rpydata.Input(db_path=db_path, conf_path=config_path)
    assert input_data is not None


@pytest.mark.unit
def test_input_initialization_single_path(setup_data):
    db_path, config_path = setup_data
    p = Path(db_path).parent
    input_data = rpydata.Input(path=p)
    assert input_data is not None


@pytest.mark.unit
def test_input_initialization_invalid_db(setup_config):
    config_path = setup_config
    with pytest.raises(FileNotFoundError, match="Database file not found"):
        rpydata.Input(db_path="invalid.db", conf_path=config_path)


@pytest.mark.unit
def test_input_initialization_invalid_conf(setup_db):
    db_path = setup_db
    with pytest.raises(FileNotFoundError, match="Config file not found at"):
        rpydata.Input(db_path=db_path, conf_path="invalid.conf")


@pytest.fixture
def input_data(setup_data):
    db_path, config_path = setup_data
    input_data = rpydata.Input(db_path=db_path, conf_path=config_path)
    yield input_data


@pytest.mark.unit
def test_repr(input_data):
    repr_str = repr(input_data)
    assert "Input" in repr_str
    assert "db_path" in repr_str
    assert "conf_path" in repr_str


@pytest.mark.unit
def test_get_interventions(input_data):
    interventions = input_data.get_interventions()
    expected_interventions = [
        'no_treatment', 'early_buprenorphine', 'buprenorphine', 'post_buprenorphine']
    assert isinstance(interventions, list)
    assert set(interventions) == set(expected_interventions)


@pytest.mark.unit
def test_get_behaviors(input_data):
    behaviors = input_data.get_behaviors()
    expected_behaviors = ['active_injection', 'nonactive_injection']
    assert isinstance(behaviors, list)
    assert set(behaviors) == set(expected_behaviors)


@pytest.mark.unit
def test_get_cohorts(input_data):
    col_names, results = input_data.get_cohorts()
    expected_col_names = [
        "id", "description", "background_mortality_sample", "behavior_transition_sample", "initial_population_sample",
        "intervention_transition_sample", "overdose_sample", "overdose_fatality_sample", "population_change_sample", "smr_sample"
    ]
    expected_results = [1, "Test Cohort 1", 1, 1, 1, 1, 1, 1, 1, 1]
    assert set(expected_col_names) == set(col_names)
    assert expected_results == list(results[0])


@pytest.mark.unit
def test_select_parameter_intervention(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)


@pytest.mark.unit
def test_select_parameter_behavior(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)


@pytest.mark.unit
def test_select_parameter_initial_cohort(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)


@pytest.mark.unit
def test_select_parameter_migrating_cohort(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.MIGRATION_COHORT)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)


@pytest.mark.unit
def test_select_parameter_overdose(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.OVERDOSE_PROBABILITY)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)


@pytest.mark.unit
def test_select_parameter_fatal_overdose(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.OVERDOSE_FATALITY_PROBABILITY)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)


@pytest.mark.unit
def test_select_parameter_background_mortality(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.BACKGROUND_DEATH_PROBABILITY)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)


@pytest.mark.unit
def test_select_parameter_smr(input_data):
    param = rpydata.Parameter(
        rpydata.ParameterType.STANDARD_MORTALITY_RATIO)
    result = input_data.select_parameter(param, cohort_id=1, time=1)
    assert isinstance(result, np.ndarray)
    print(result)
