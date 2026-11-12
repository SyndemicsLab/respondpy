################################################################################
# File: test_simulation.py                                                     #
# Project: respondpy                                                           #
# Created Date: 2026-02-26                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-11-12                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

# pylint: disable=attribute-defined-outside-init, redefined-outer-name

# Disabling comments from pylint because pytest fixtures don't follow the same convention.

import sqlite3
from configparser import ConfigParser
import importlib
import threading

import numpy as np
import pytest

import respondpy as rpy


build_module = importlib.import_module("respondpy.build")


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
    cfg["simulation"] = {
        "duration": "1",
        "parameter_change_times": "1",
        "stratify_entering_cohort": "false",
    }

    cfg["output"] = {
        "build_summary_stats": "true",
        "save_state_history": "true",
        "timesteps_to_report": "1",
    }

    with mem_str.open("w") as configfile:
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


def _add_test_cohorts(input_data, count):
    input_data.insert_cohorts(
        [
            (f"Parallel test cohort {cohort_id}", 1, 1, 1, 1, 1, 1, 1, 1)
            for cohort_id in range(2, count + 1)
        ]
    )
    return list(range(1, count + 1))


def _model_marked_by_cohort(cohort_id):
    model = rpy.Model("markov", rpy.RuntimeConfig())
    model.set_state(np.array([float(cohort_id)]))
    return model


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


@pytest.mark.unit
def test_parallel_build_preserves_order_and_processor_count(
    setup_data, tmp_path, monkeypatch
):
    db, cfg = setup_data
    input_data = rpy.data.Input(db_path=db, conf_path=cfg)
    _add_test_cohorts(input_data, 8)
    requested = [8, 2, 7, 1, 8, 4, 3, 6]
    barrier = threading.Barrier(2)
    lock = threading.Lock()
    observations = []

    def fake_build_model(
        worker_input,
        cohort_id,
        *,
        processor_count=None,
        log_name="respond",
        log_file="respond.log",
    ):
        assert cohort_id in worker_input.get_cohort_ids()
        barrier.wait(timeout=5)
        with lock:
            observations.append(
                (
                    threading.get_ident(),
                    id(worker_input._connection),
                    cohort_id,
                    processor_count,
                )
            )
        return _model_marked_by_cohort(cohort_id)

    monkeypatch.setattr(build_module, "cpu_count", lambda: 2)
    monkeypatch.setattr(build_module, "build_model", fake_build_model)

    simulation = build_module.build_simulation(
        input_data,
        build_workers=2,
        processor_count=3,
        cohort_ids=requested,
        log_name="parallel-order-test",
        log_file=str(tmp_path / "parallel-order.log"),
    )

    actual = [
        int(simulation.get_model(index).get_state()[0])
        for index in range(len(requested))
    ]
    assert actual == requested
    assert len({item[0] for item in observations}) == 2
    assert all(item[1] != id(input_data._connection) for item in observations)
    assert [item[2] for item in observations].count(8) == 2
    assert all(item[3] == 3 for item in observations)
    assert simulation.get_execution_config().total_threads == 3


@pytest.mark.unit
def test_parallel_build_closes_worker_inputs_on_failure(
    setup_data, tmp_path, monkeypatch
):
    db, cfg = setup_data
    input_data = rpy.data.Input(db_path=db, conf_path=cfg)
    cohort_ids = _add_test_cohorts(input_data, 8)
    worker_inputs = []
    lock = threading.Lock()
    original_factory = rpy.data.Input._new_worker_input

    def track_worker_input(source):
        worker_input = original_factory(source)
        with lock:
            worker_inputs.append(worker_input)
        return worker_input

    def failing_build_model(
        worker_input,
        cohort_id,
        *,
        processor_count=None,
        log_name="respond",
        log_file="respond.log",
    ):
        if cohort_id == 3:
            raise RuntimeError("injected worker failure")
        return _model_marked_by_cohort(cohort_id)

    monkeypatch.setattr(build_module, "cpu_count", lambda: 2)
    monkeypatch.setattr(
        rpy.data.Input, "_new_worker_input", track_worker_input
    )
    monkeypatch.setattr(build_module, "build_model", failing_build_model)

    with pytest.raises(RuntimeError, match="injected worker failure"):
        build_module.build_simulation(
            input_data,
            build_workers=2,
            cohort_ids=cohort_ids,
            log_name="parallel-failure-test",
            log_file=str(tmp_path / "parallel-failure.log"),
        )

    assert worker_inputs
    assert all(worker_input._connection is None for worker_input in worker_inputs)


@pytest.mark.unit
def test_input_subclass_uses_serial_build_fallback(setup_data, monkeypatch):
    db, cfg = setup_data

    class CustomInput(rpy.data.Input):
        def _new_worker_input(self):
            raise AssertionError("parallel worker factory must not be used")

    input_data = CustomInput(db_path=db, conf_path=cfg)
    cohort_ids = _add_test_cohorts(input_data, 8)
    monkeypatch.setattr(build_module, "cpu_count", lambda: 2)

    simulation = build_module.build_simulation(
        input_data, cohort_ids=cohort_ids, build_workers=2
    )

    assert len(simulation.get_model_names()) == len(cohort_ids)
