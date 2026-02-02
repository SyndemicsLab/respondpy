################################################################################
# File: test.py                                                                #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-02                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""
Smoke Tests to ensure RESPOND compiled. 
Run with `uv run python -m respondpy.test`.
"""

from __future__ import annotations

import unittest
import numpy as np

import respondpy as rpy


class TestRespondPy(unittest.TestCase):
    state = [10, 20, 30]

    def test_markov(self) -> None:
        markov = rpy.Markov()
        markov.set_state(self.state)
        np.testing.assert_array_equal(self.state, markov.get_state())

    # def test_add_transition(self) -> None:
    #     markov = rpy.Markov()
    #     markov.set_state(self.state)

    #     def temp_callable(s: rpy.vector_1d, t: rpy.vector_of_matrices, h: rpy.HistoryStamp) -> rpy.vector_1d:
    #         return s

    #     data = list(np.array([1.0, 0.9, 0.8]))

    #     transition = (temp_callable, data)

    #     markov.add_transition(transition)
    #     markov.run(1)


if __name__ == "__main__":
    unittest.main("respondpy.test", warnings="error")
