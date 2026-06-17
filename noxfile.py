################################################################################
# File: noxfile.py                                                             #
# Project: respondpy                                                           #
# Created Date: 2026-04-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-04-08                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from __future__ import annotations

import nox  # type: ignore[import-not-found]  # pylint: disable=import-error


@nox.session(python=["3.12"], venv_backend="uv")
def pylint(session: nox.Session) -> None:
    """Run pylint checks for source code only."""
    session.env["PYTHONPATH"] = "src"
    session.install("pylint", "numpy", "polars")
    session.run("pylint", "src/respondpy")


@nox.session(python=["3.12"], venv_backend="uv")
def benchmark(session: nox.Session) -> None:
    """Run end-to-end benchmarks (not included in normal test runs).

    Results are printed to stdout. Optionally pass --benchmark-save=<name>
    to persist results for later comparison:

        uv run nox -s benchmark -- --benchmark-save=baseline
    """
    session.env["PYTHONPATH"] = "build/respondpy"
    session.install("--group=benchmark", ".")
    session.run(
        "pytest",
        "benchmarks/",
        "--benchmark-only",
        "--benchmark-columns=min,mean,stddev,rounds",
        "--benchmark-sort=name",
        "-v",
        *session.posargs,
    )
