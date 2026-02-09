################################################################################
# File: test_smoke.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-05                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""
Smoke Tests to ensure RESPOND compiled. 
Run with `uv run pytest -m smoke`.
"""

from __future__ import annotations

import pytest
import numpy as np

import respondpy as rpy


@pytest.mark.smoke
def test_markov() -> None:
    state = np.array([10, 20, 30])
    markov = rpy.Markov()
    markov.set_state(state)
    np.testing.assert_array_equal(state, markov.get_state())


@pytest.mark.smoke
def test_add_transition() -> None:
    markov = rpy.Markov()
    t = rpy.Transition()

    def test_callback(a, b, c):
        return a

    t.set_callback(test_callback)
    t.transition_matrices = [np.array([1.0, 1.0])]
    markov.add_transition(t)

#     def temp_callable(s: rpy.vector_1d, t: rpy.vector_of_matrices, h: rpy.HistoryStamp) -> rpy.vector_1d:
#         return s

#     data = list(np.array([1.0, 0.9, 0.8]))

#     transition = (temp_callable, data)

#     markov.add_transition(transition)
#     markov.run(1)
