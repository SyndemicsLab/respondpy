################################################################################
# File: conftest.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-11-11                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-11-12                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

import pytest


CONFIG_PATH = Path(__file__).with_name("benchmark_config.toml")


@dataclass(frozen=True)
class LocalInputs:
    input_db: Path
    sim_config: Path


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("respondpy benchmark")
    group.addoption(
        "--benchmark-data-root",
        type=Path,
        help="Directory containing the required input.db and sim.conf files.",
    )
    group.addoption(
        "--benchmark-rounds",
        type=int,
        help="Override the configured number of measured rounds.",
    )


@pytest.fixture(scope="session")
def local_inputs(request: pytest.FixtureRequest) -> LocalInputs:
    data_root = request.config.getoption("--benchmark-data-root")
    if data_root is None:
        pytest.fail(
            "Pass --benchmark-data-root with the directory containing "
            "input.db and sim.conf."
        )

    root = data_root.expanduser().resolve()
    if not root.is_dir():
        pytest.fail(f"Benchmark data directory does not exist: {root}")

    paths = LocalInputs(
        input_db=root / "input.db",
        sim_config=root / "sim.conf",
    )
    missing = [
        path.name
        for path in (paths.input_db, paths.sim_config)
        if not path.is_file()
    ]
    if missing:
        pytest.fail(
            f"Benchmark data directory is missing required files: "
            f"{', '.join(missing)}"
        )
    return paths


@pytest.fixture(scope="session")
def benchmark_rounds(request: pytest.FixtureRequest) -> int:
    with CONFIG_PATH.open("rb") as config_file:
        rounds = tomllib.load(config_file)["benchmark"]["rounds"]

    override = request.config.getoption("--benchmark-rounds")
    if override is not None:
        rounds = override
    if not isinstance(rounds, int) or rounds <= 0:
        pytest.fail("Benchmark rounds must be a positive integer.")
    return rounds
