################################################################################
# File: test_data_input.py                                                     #
# Project: respondpy                                                           #
# Created Date: 2026-06-10                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-25                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import sqlite3
import uuid
from configparser import ConfigParser
from pathlib import Path

import pytest
import numpy as np
import polars as pl

import respondpy as rpy
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
def test_get_interventions_id_maps(input_data):
    interventions = input_data.get_intervention_id_maps()
    expected_interventions = {
        1: 'no_treatment', 2: 'early_buprenorphine', 3: 'buprenorphine', 4: 'post_buprenorphine'}
    assert isinstance(interventions, dict)
    assert interventions == expected_interventions


@pytest.mark.unit
def test_get_behaviors_id_maps(input_data):
    behaviors = input_data.get_behavior_id_maps()
    expected_behaviors = {1: 'active_injection', 2: 'nonactive_injection'}
    assert isinstance(behaviors, dict)
    assert behaviors == expected_behaviors


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
def test_get_cohort_ids(input_data):
    ids = input_data.get_cohort_ids()
    expected_ids = [1]
    assert expected_ids == ids


@pytest.mark.unit
def test_select_parameter_is_cached(input_data):
    param = rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT)

    original_sample_lookup = input_data._get_sample_id_for_parameter
    original_parameter_fill = input_data._get_parameter_filled
    calls = {"sample_lookup": 0, "parameter_fill": 0}

    def counting_sample_lookup(param_obj, cohort_id=1):
        calls["sample_lookup"] += 1
        return original_sample_lookup(param_obj, cohort_id)

    def counting_parameter_fill(param_obj, sample_id=1, time=1):
        calls["parameter_fill"] += 1
        return original_parameter_fill(param_obj, sample_id, time)

    input_data._get_sample_id_for_parameter = counting_sample_lookup
    input_data._get_parameter_filled = counting_parameter_fill

    first = input_data.select_parameter(param, cohort_id=1, time=1)
    second = input_data.select_parameter(param, cohort_id=1, time=1)

    assert isinstance(first, np.ndarray)
    assert np.array_equal(first, second)
    assert calls["sample_lookup"] == 1
    assert calls["parameter_fill"] == 1


@pytest.mark.unit
def test_complete_parameter_avoids_sort(input_data, monkeypatch):
    param = rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT)
    sample_id = input_data._get_sample_id_for_parameter(param, cohort_id=1)

    def fail_sort(*args, **kwargs):
        raise AssertionError("complete parameter tables should bypass sort_dataframes")

    monkeypatch.setattr("respondpy.data.input.sort_dataframes", fail_sort)

    lf = input_data._get_parameter_filled(param, sample_id=sample_id, time=1)
    assert isinstance(lf, pl.LazyFrame)
    assert lf.select(pl.len()).collect().item() == len(input_data.get_interventions()) * len(input_data.get_behaviors())


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


@pytest.mark.unit
def test_input_initialization_requires_complete_paths(setup_db):
    db_path = setup_db
    with pytest.raises(ValueError, match="Must provide either a path"):
        rpydata.Input(db_path=db_path)


@pytest.mark.unit
def test_get_connection_raises_when_missing(input_data):
    input_data._connection = None
    with pytest.raises(ConnectionError, match="No database connection established"):
        input_data._get_connection()


@pytest.mark.unit
def test_check_valid_list_edge_cases(input_data):
    assert input_data._check_valid_list([], 2) is False
    assert input_data._check_valid_list([(1, 2)], 3) is False
    assert input_data._check_valid_list([(1, 2)], 2) is True


@pytest.mark.unit
def test_connect_and_executemany_rejects_bad_shapes(input_data):
    with pytest.raises(ValueError, match="Expected list of tuples with 2 items each"):
        input_data._connect_and_executemany(
            [(1,)],
            "INSERT INTO intervention(id, name) VALUES (?, ?)"
        )


@pytest.mark.unit
def test_get_sample_ids_by_table_valid_and_invalid(input_data):
    assert input_data._get_sample_ids_by_table("initial_population") == [1]
    with pytest.raises(ValueError, match="does not exist"):
        input_data._get_sample_ids_by_table("not_a_real_table")


@pytest.mark.unit
def test_get_sample_id_for_parameter_missing_cohort_raises(input_data):
    with pytest.raises(ValueError, match="No sample ID found"):
        input_data._get_sample_id_for_parameter(
            rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT),
            cohort_id=999,
        )


@pytest.mark.unit
def test_select_parameter_raw_returns_numpy(input_data):
    result = input_data.select_parameter(
        rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT),
        cohort_id=1,
        time=1,
        raw=True,
    )
    assert isinstance(result, np.ndarray)
    assert result.shape[0] > 0


@pytest.mark.unit
def test_extract_values_rejects_invalid_parameter(input_data):
    class InvalidParameter:
        def get_value_column_name(self):
            return "probability"

        def is_state_vector_operation(self):
            return False

        def is_transition_matrix_operation(self):
            return False

    with pytest.raises(ValueError, match="Invalid parameter applied"):
        input_data._extract_values(
            InvalidParameter(),
            pl.LazyFrame({"probability": [1.0]}),
            n=1,
        )


@pytest.mark.unit
def test_zero_invalid_transitions_passthrough_for_non_transition_param(input_data):
    transition_matrix = pl.DataFrame(
        {
            "initial_intervention": ["A"],
            "new_intervention": ["B"],
            "initial_behavior": ["X"],
            "new_behavior": ["Y"],
            "probability": [0.5],
        }
    )

    out = input_data._zero_invalid_transitions(
        rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT),
        transition_matrix,
    )
    assert out.equals(transition_matrix)


@pytest.mark.unit
def test_insert_cohorts_adds_new_row(input_data):
    before_cols, before_rows = input_data.get_cohorts()
    assert "id" in before_cols

    input_data.insert_cohorts([
        ("Second Cohort", 1, 1, 1, 1, 1, 1, 1, 1)
    ])

    _, after_rows = input_data.get_cohorts()
    assert len(after_rows) == len(before_rows) + 1


@pytest.mark.unit
def test_insert_parameter_adds_sample_row(input_data):
    parameter = rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT)
    input_data.select_parameter(parameter, cohort_id=1)
    assert input_data._parameter_cache

    input_data.insert_parameter(parameter, [(2, 1, 1, 42.0)])

    sample_ids = input_data._get_sample_ids_by_table("initial_population")
    assert 2 in sample_ids
    assert not input_data._parameter_cache


@pytest.mark.unit
def test_input_logging_writes_to_backend_file(setup_data) -> None:
    db_path, config_path = setup_data
    log_file = Path(db_path).parent / "respond-input.log"
    logger_name = f"respond-input-{uuid.uuid4()}"

    input_data = rpydata.Input(
        db_path=db_path,
        conf_path=config_path,
        log_name=logger_name,
        log_file=log_file,
    )
    rpy.logging.log_info(logger_name, "python-input-info-message")
    rpy.logging.log_warning(logger_name, "python-input-warning-message")
    rpy.logging.flush_all_loggers()
    assert log_file.exists()

    contents = log_file.read_text()
    assert "python-input-info-message" in contents
    assert "python-input-warning-message" in contents
