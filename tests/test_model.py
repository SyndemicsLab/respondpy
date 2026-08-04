################################################################################
# File: test_model.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-06-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-10                                                    #
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
def setup_config_missing_change_time(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "sim_missing_change_time.conf"
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


@pytest.mark.unit
def test_build_model(setup_data) -> None:
    db, cfg = setup_data
    inp = rpy.data.Input(db_path=db, conf_path=cfg)
    sim = rpy.build_simulation(inp, cohort_ids=[1])
    m = sim.get_model(0)
    assert isinstance(m, rpy.Model)


@pytest.mark.unit
def test_build_model_raises_when_change_time_rows_missing(
    setup_db,
    setup_config_missing_change_time,
) -> None:
    inp = rpy.data.Input(db_path=setup_db, conf_path=setup_config_missing_change_time)

    with pytest.raises(
        ValueError,
        match=r"Missing time-varying parameter rows in database: .*time=52",
    ):
        rpy.build_simulation(inp, cohort_ids=[1])


@pytest.mark.unit
def test_model_default_histories_can_be_created() -> None:
    model = rpy.Model("markov")
    model.set_state(np.array([1.0, 2.0, 3.0]))
    model.create_default_histories()

    histories = model.get_histories()
    assert isinstance(histories, dict)
    assert "state" in histories
    assert isinstance(histories["state"], rpy.History)


@pytest.mark.unit
def test_model_set_and_get_state_roundtrip() -> None:
    model = rpy.Model("markov")
    expected = np.array([3.0, 2.0, 1.0])

    model.set_state(expected)

    np.testing.assert_array_equal(model.get_state(), expected)
