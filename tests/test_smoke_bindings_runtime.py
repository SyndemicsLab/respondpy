################################################################################
# File: test_smoke_bindings_runtime.py                                         #
# Project: respondpy                                                           #
# Created Date: 2026-07-22                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-09-25                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""Smoke tests validating pybind runtime contracts for core bindings."""

from __future__ import annotations

from copy import copy
from concurrent.futures import ThreadPoolExecutor
import math
import uuid

import numpy as np
import pytest

import respondpy as rpy
from respondpy.history import HistoryMode


@pytest.mark.smoke
def test_transition_execute_returns_state_and_history_tuple() -> None:
    """Transition.execute should return both the updated state and history map."""
    transition = rpy.Transition("migration")
    transition.add_matrix(np.zeros((3, 1)))
    input_state = np.array([1.0, 2.0, 3.0])

    result = transition.execute(input_state, {})

    assert isinstance(result, tuple), (
        "Expected Transition.execute to return a tuple of "
        "(StateVector, history_map)."
    )
    assert len(result) == 2, (
        "Expected Transition.execute tuple to have exactly 2 elements: "
        "state and history map."
    )

    output_state, output_history = result
    np.testing.assert_equal(
        output_state.shape,
        input_state.shape,
        err_msg="Expected output state shape to match input state shape.",
    )
    assert isinstance(output_history, dict), (
        "Expected Transition.execute second return value to be a dict-like "
        "history mapping."
    )


@pytest.mark.smoke
def test_history_mode_members_and_latest_timestep_method_are_exposed() -> None:
    """History bindings should expose enum members and latest timestep accessor."""
    assert hasattr(HistoryMode, "kSnapshot"), (
        "Expected HistoryMode to expose enum member 'kSnapshot'."
    )
    assert hasattr(HistoryMode, "kAccumulated"), (
        "Expected HistoryMode to expose enum member 'kAccumulated'."
    )

    history = rpy.History("state")
    assert hasattr(history, "get_latest_recorded_timestep"), (
        "Expected History to expose method 'get_latest_recorded_timestep'."
    )


@pytest.mark.smoke
def test_runtime_configuration_bindings_are_mutable_and_nested() -> None:
    """Runtime configuration structs should expose defaults and mutable fields."""
    execution = rpy.ExecutionConfig()
    logging = rpy.LoggingConfig()
    runtime = rpy.RuntimeConfig()

    assert execution.total_threads == 0
    assert execution.eigen_threads == 1
    assert execution.run_models_concurrently is False
    assert logging.logger_name == "respond"
    assert logging.file_path == "respond.log"
    assert logging.use_shared_sink is False

    execution.total_threads = 4
    execution.eigen_threads = 1
    execution.run_models_concurrently = True
    logging.logger_name = "test"
    logging.file_path = "test.log"
    logging.use_shared_sink = True
    runtime.execution = execution
    runtime.logging = logging

    assert rpy.config.ExecutionConfig is rpy.ExecutionConfig
    assert runtime.execution.total_threads == 4
    assert runtime.execution.run_models_concurrently is True
    assert runtime.logging.logger_name == "test"
    assert runtime.logging.use_shared_sink is True


@pytest.mark.smoke
def test_logging_api_parity(tmp_path) -> None:
    """Logging bindings should expose the hotfix API and status semantics."""
    logging = rpy.logging
    suffix = uuid.uuid4().hex
    logger_name = f"logging_parity_{suffix}"
    logfile = tmp_path / "configured.log"

    config = rpy.LoggingConfig()
    config.logger_name = logger_name
    config.file_path = str(logfile)

    assert logging.configure_logger(config) == logging.CreationStatus.kSuccess
    assert logging.check_logger_exists(
        logger_name) == logging.CreationStatus.kExists
    assert logger_name in logging.get_logger_info(logger_name)

    assert logging.configure_logger(config) == logging.CreationStatus.kExists
    conflicting = rpy.LoggingConfig()
    conflicting.logger_name = logger_name
    conflicting.file_path = str(tmp_path / "conflicting.log")
    assert logging.configure_logger(
        conflicting) == logging.CreationStatus.kError

    logging.set_logger_level(logger_name, 2)
    logging.log_info(logger_name, "configured message")
    logging.log_warning(logger_name, "warning message")
    logging.log_error(logger_name, "error message")
    logging.log_debug(logger_name, "debug message")

    shared_logfile = tmp_path / "shared.log"
    shared_name_a = f"shared_a_{suffix}"
    shared_name_b = f"shared_b_{suffix}"
    assert (
        logging.create_shared_file_sink(str(shared_logfile))
        == logging.CreationStatus.kSuccess
    )
    assert (
        logging.create_shared_file_sink(str(shared_logfile))
        == logging.CreationStatus.kExists
    )
    assert (
        logging.create_shared_logger(shared_name_a)
        == logging.CreationStatus.kSuccess
    )
    assert (
        logging.create_shared_logger(shared_name_b)
        == logging.CreationStatus.kSuccess
    )
    logging.log_info(shared_name_a, "shared message A")
    logging.log_info(shared_name_b, "shared message B")

    concurrent_names = [
        f"shared_concurrent_{suffix}_{index}" for index in range(4)]

    def create_and_write(name: str) -> logging.CreationStatus:
        status = logging.create_shared_logger(name)
        logging.log_info(name, f"concurrent message {name}")
        return status

    with ThreadPoolExecutor(max_workers=len(concurrent_names)) as executor:
        statuses = list(executor.map(create_and_write, concurrent_names))

    assert statuses == [logging.CreationStatus.kSuccess] * \
        len(concurrent_names)

    original_pattern = logging.get_log_pattern()
    logging.set_log_pattern(logging.LogPattern.kDetailed)
    assert logging.get_log_pattern() == logging.LogPattern.kDetailed
    logging.set_log_pattern(original_pattern)
    logging.set_flush_interval(0)
    logging.flush_all_loggers()
    logging.flush_all_loggers()

    assert "configured message" in logfile.read_text(encoding="utf-8")
    shared_output = shared_logfile.read_text(encoding="utf-8")
    assert "shared message A" in shared_output
    assert "shared message B" in shared_output
    for name in concurrent_names:
        assert f"concurrent message {name}" in shared_output
    assert (
        logging.check_logger_exists(f"missing_{suffix}")
        == logging.CreationStatus.kNotCreated
    )


@pytest.mark.smoke
def test_model_accepts_runtime_configuration(tmp_path) -> None:
    """Model should support construction with shared runtime settings."""
    runtime = rpy.RuntimeConfig()
    runtime.logging.logger_name = "model_runtime_config"
    runtime.logging.file_path = str(tmp_path / "model.log")

    model = rpy.Model("markov", runtime)

    assert isinstance(model, rpy.Model)
    assert model.get_name() == "markov"


@pytest.mark.smoke
def test_simulation_runtime_configuration_accessors_and_constructors(
    tmp_path,
) -> None:
    """Simulation should expose runtime settings and compatibility constructors."""
    runtime = rpy.RuntimeConfig()
    runtime.execution.total_threads = 2
    runtime.execution.run_models_concurrently = True
    runtime.logging.logger_name = "simulation_runtime_config"
    runtime.logging.file_path = str(tmp_path / "simulation.log")

    simulation = rpy.Simulation(runtime)
    execution = simulation.get_execution_config()
    returned_runtime = simulation.get_runtime_config()

    assert execution.total_threads == 2
    assert execution.run_models_concurrently is True
    assert returned_runtime.logging.logger_name == "simulation_runtime_config"

    replacement_execution = rpy.ExecutionConfig()
    replacement_execution.total_threads = 3
    simulation.set_execution_config(replacement_execution)
    assert simulation.get_execution_config().total_threads == 3

    runnable = rpy.Simulation()
    runnable.create_new_model("markov")
    runnable.run(1)

    replacement_runtime = rpy.RuntimeConfig()
    replacement_runtime.logging.logger_name = "simulation_runtime_replaced"
    replacement_runtime.logging.file_path = str(tmp_path / "replaced.log")
    runnable.set_runtime_config(replacement_runtime)
    assert (
        runnable.get_runtime_config().logging.logger_name
        == "simulation_runtime_replaced"
    )

    legacy = rpy.Simulation(
        "simulation_legacy_config",
        str(tmp_path / "legacy.log"),
        rpy.ExecutionConfig(),
    )
    assert isinstance(legacy, rpy.Simulation)


@pytest.mark.smoke
def test_runtime_simulation_validation_and_concurrency() -> None:
    """Simulation should enforce duration and Eigen concurrency constraints."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    for duration in (0, -2):
        with pytest.raises(ValueError, match="Simulation duration must be positive"):
            simulation.run(duration)

    for duration in (0, -1):
        with pytest.raises(ValueError, match="Simulation duration must be positive"):
            simulation.set_duration(duration)

    concurrent = rpy.Simulation()
    concurrent.create_new_model("markov")
    concurrent.create_new_model("markov")
    runtime = concurrent.get_runtime_config()
    runtime.execution.run_models_concurrently = True
    runtime.execution.eigen_threads = 2
    runtime.execution.total_threads = 2
    concurrent.set_runtime_config(runtime)

    with pytest.raises(
        ValueError,
        match="Concurrent model execution requires eigen_threads <= 1",
    ):
        concurrent.run(1)

    runtime.execution.eigen_threads = 1
    concurrent.set_runtime_config(runtime)
    concurrent.run(1)

    def run_concurrent_simulation() -> int:
        worker = rpy.Simulation()
        worker.create_new_model("markov")
        worker.create_new_model("markov")
        worker_runtime = worker.get_runtime_config()
        worker_runtime.execution.run_models_concurrently = True
        worker_runtime.execution.eigen_threads = 1
        worker_runtime.execution.total_threads = 2
        worker.set_runtime_config(worker_runtime)
        worker.run(1)
        return len(worker.get_models())

    with ThreadPoolExecutor(max_workers=2) as executor:
        assert list(executor.map(lambda _: run_concurrent_simulation(), range(2))) == [
            2,
            2,
        ]


@pytest.mark.smoke
def test_runtime_deferred_validation_and_missing_logger(capfd) -> None:
    """Deferred transition checks and missing logger handling should be clear."""
    transition = rpy.Transition("migration")
    transition.add_matrix(np.zeros((2, 1)))

    with pytest.raises(RuntimeError, match="matrix size mismatch"):
        transition.execute(np.array([1.0, 2.0, 3.0]), {})

    timestep = rpy.Timestep()
    timestep.create_transition("migration")
    timestep.add_matrix_to_transition("migration", np.zeros((2, 1)))
    with pytest.raises(RuntimeError, match="matrix size mismatch"):
        timestep.get_transition("migration").execute(
            np.array([1.0, 2.0, 3.0]), {}
        )

    missing_name = f"missing_logger_{uuid.uuid4().hex}"
    assert missing_name in rpy.logging.get_logger_info(missing_name)
    rpy.logging.log_info(missing_name, "missing logger message")
    rpy.logging.flush_all_loggers()
    captured = capfd.readouterr()
    assert missing_name in captured.err
    assert "not persisted" in captured.err


@pytest.mark.smoke
def test_history_ordering_copy_and_discount_behavior() -> None:
    """History copies and cost-effectiveness discounting should be stable."""
    history = rpy.History("runtime_ordering")
    history.add_state(np.array([3.0]), 3)
    history.add_state(np.array([1.0]), 1)
    history.add_state(np.array([2.0]), 2)

    assert list(history.get_recorded_timesteps()) == [1, 2, 3]
    cloned = copy(history)
    cloned.add_state(np.array([9.0]), 1)
    assert history.get_state_map()[1][0] == 1.0
    assert cloned.get_state_map()[1][0] == 9.0

    result = rpy.discount(np.array([52.0]), 0.05, 52, True, 52.0)
    expected = 52.0 / math.pow(1.0 + 0.05 / 52.0, 52)
    np.testing.assert_allclose(result, np.array([expected]))


@pytest.mark.smoke
def test_simulation_create_new_model_returns_model_and_registers_model() -> None:
    """Simulation.create_new_model should return a cloned Model instance."""
    simulation = rpy.Simulation()
    created_model = simulation.create_new_model("markov")

    assert isinstance(created_model, rpy.Model), (
        "Expected Simulation.create_new_model to return a Model instance."
    )
    assert created_model.get_name() == "markov", (
        "Expected returned model to use the requested model type name."
    )
    assert simulation.get_model_names() == ["markov"], (
        "Expected simulation to register one canonical model name: 'markov'."
    )
    assert isinstance(simulation.get_model(0), rpy.Model), (
        "Expected get_model(0) to return a Model instance after creation."
    )


@pytest.mark.smoke
def test_simulation_get_model_returns_live_mutable_model_reference() -> None:
    """Mutating a model from get_model should update the simulation-owned model."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    expected_state = np.array([3.0, 2.0, 1.0])
    model = simulation.get_model(0)
    model.set_state(expected_state)

    np.testing.assert_array_equal(
        simulation.get_model(0).get_state(),
        expected_state,
        err_msg="Expected get_model to expose a live simulation-owned model.",
    )


@pytest.mark.smoke
def test_simulation_set_model_replaces_model_by_index() -> None:
    """set_model(index, model) should replace the stored model state."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    replacement = rpy.Model("markov")
    replacement_state = np.array([7.0, 8.0, 9.0])
    replacement.set_state(replacement_state)

    simulation.set_model(0, replacement)

    np.testing.assert_array_equal(
        simulation.get_model(0).get_state(),
        replacement_state,
        err_msg="Expected set_model to replace the simulation model at index.",
    )


@pytest.mark.smoke
def test_simulation_index_setitem_replaces_model_by_index() -> None:
    """Simulation[index] assignment should replace the stored model."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    replacement = rpy.Model("markov")
    replacement_state = np.array([4.0, 5.0, 6.0])
    replacement.set_state(replacement_state)

    simulation[0] = replacement

    np.testing.assert_array_equal(
        simulation[0].get_state(),
        replacement_state,
        err_msg="Expected __setitem__ to replace the simulation model at index.",
    )


@pytest.mark.smoke
def test_binding_failure_messages_follow_expected_patterns() -> None:
    """Binding exceptions should surface informative message patterns."""
    simulation = rpy.Simulation()
    simulation.create_new_model("markov")

    with pytest.raises(Exception, match=r"(?i)(out of bounds|index)"):
        simulation.get_model(999)

    timestep = rpy.Timestep()
    with pytest.raises(Exception, match=r"(?i)(not found|transition)"):
        timestep.get_transition("missing")

    with pytest.raises(TypeError, match=r"(?i)incompatible constructor arguments"):
        _ = rpy.Simulation(1)  # type: ignore[arg-type]


@pytest.mark.smoke
def test_timestep_add_transition_clones_input_transition() -> None:
    """Timestep.add_transition should clone, not alias, the input transition."""
    timestep = rpy.Timestep()
    source_transition = rpy.Transition("migration")
    first_matrix = np.array([[0.5], [0.5], [0.0]])
    source_transition.add_matrix(first_matrix)

    timestep.add_transition(source_transition)

    second_matrix = np.array([[0.2], [0.3], [0.5]])
    source_transition.add_matrix(second_matrix)

    stored_transition = timestep.get_transition(0)
    stored_matrices = stored_transition.get_matrices()
    assert len(stored_matrices) == 1, (
        "Expected timestep-owned transition to remain independent after "
        "mutating the caller-owned transition."
    )
    np.testing.assert_allclose(stored_matrices[0], first_matrix)


@pytest.mark.smoke
def test_timestep_index_access_supports_get_and_set() -> None:
    """Timestep index operators should expose mutable get/set semantics."""
    timestep = rpy.Timestep()
    timestep.create_transition("migration")
    timestep.create_transition("behavior")

    replacement = rpy.Transition("overdose", "overdose")
    timestep[1] = replacement

    assert timestep[0].get_name() == "migration", (
        "Expected __getitem__ to return transition by index."
    )
    assert timestep[1].get_name() == replacement.get_name(), (
        "Expected __setitem__ to replace transition slot by index."
    )
