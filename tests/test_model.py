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

from __future__ import annotations


import sqlite3
from configparser import ConfigParser

import pytest

import respondpy as rpy


class DummyTransition:
    def __init__(self, label: str) -> None:
        self.label = label

    def copy(self) -> DummyTransition:
        return DummyTransition(self.label)


class DummyModel:
    def __init__(self) -> None:
        self.transitions: list[DummyTransition] = []

    def add_transition(self, transition: DummyTransition) -> None:
        self.transitions.append(transition)


class DummyInput:
    def __init__(self, duration: int, parameter_change_times: str) -> None:
        cfg = ConfigParser()
        cfg["simulation"] = {
            "duration": str(duration),
            "parameter_change_times": parameter_change_times,
        }
        self.config = cfg


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
def test_build_model(setup_data) -> None:
    db, cfg = setup_data
    inp = rpy.data.Input(db_path=db, conf_path=cfg)
    m = rpy.build_model(inp, 1)
    assert isinstance(m, rpy.Model)


@pytest.mark.unit
def test_build_model_transitions_rebuilds_on_change_times(
        monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[int] = []

    def fake_build_timestep_transition(
            timestep: int,
            _input_data: DummyInput,
            _cohort_id: int,
    ) -> list[DummyTransition]:
        calls.append(timestep)
        return [DummyTransition(f"t{timestep}")]

    monkeypatch.setattr(rpy.model, "build_timestep_transition",
                        fake_build_timestep_transition)

    model = DummyModel()
    data = DummyInput(duration=4, parameter_change_times="1,3")

    out = rpy.model.build_model_transitions(model, data, cohort_id=1)

    assert out is model
    # Initial build at timestep 1, then rebuild when i == 3.
    assert calls == [1, 3]
    # One transition for each timestep in duration.
    assert len(model.transitions) == 4


@pytest.mark.unit
def test_add_transitions_to_model_returns_same_instance() -> None:
    model = DummyModel()
    transitions = [DummyTransition("a"), DummyTransition("b")]

    out = rpy.model.add_transitions_to_model(model, transitions)

    assert out is model
    assert [t.label for t in model.transitions] == ["a", "b"]
