################################################################################
# File: test_execute.py                                                        #
# Project: respondpy                                                           #
# Created Date: 2026-02-26                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-26                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

# pylint: disable=attribute-defined-outside-init, redefined-outer-name

# Disabling comments from pylint because pytest fixtures don't follow the same convention.

import sqlite3
from configparser import ConfigParser

import pytest

from respondpy import build_simulation


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
def setup_config():
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

    yield cfg


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
    sim = build_simulation([1], db, cfg)
    assert len(sim.get_models()) == 1
