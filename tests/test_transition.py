################################################################################
# File: test_transition.py                                                     #
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
def test_build_timestep_transition(setup_data) -> None:
    transition = rpy.Transition("migration")
    matrix = np.zeros((3, 1))

    transition.add_matrix(matrix)

    matrices = transition.get_matrices()
    assert isinstance(matrices, list)
    assert len(matrices) == 1
    np.testing.assert_array_equal(matrices[0], matrix)
