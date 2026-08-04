################################################################################
# File: test_simulation.py                                                     #
# Project: respondpy                                                           #
# Created Date: 2026-02-26                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-11                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

# pylint: disable=attribute-defined-outside-init, redefined-outer-name

# Disabling comments from pylint because pytest fixtures don't follow the same convention.

import sqlite3
from configparser import ConfigParser

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


@pytest.mark.unit
def test_build_simulation(setup_data):
    """Basic unit test to verify the simulation can be built

    Args:
        setup_data (_type_): _description_
    """
    db, cfg = setup_data
    inp = rpy.data.Input(db_path=db, conf_path=cfg)
    sim = rpy.build_simulation(inp)
    assert len(sim.get_models()) == 1


def test_build_simulation_with_cohort_id(setup_data):
    """Basic unit test to verify the simulation can be built

    Args:
        setup_data (_type_): _description_
    """
    db, cfg = setup_data
    inp = rpy.data.Input(db_path=db, conf_path=cfg)
    sim = rpy.build_simulation(inp, cohort_ids=[1])
    assert len(sim.get_models()) == 1


def test_build_simulation_with_invalid_cohort_id(setup_data):
    """Basic unit test to verify the simulation can be built

    Args:
        setup_data (_type_): _description_
    """
    db, cfg = setup_data
    inp = rpy.data.Input(db_path=db, conf_path=cfg)
    with pytest.raises(ValueError, match="Cohort IDs"):
        rpy.build_simulation(inp, cohort_ids=[2])
