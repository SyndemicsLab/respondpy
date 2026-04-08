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
