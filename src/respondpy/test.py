################################################################################
# File: test.py                                                                #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-08                                                    #
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

import respondpy as rsp


class TestRespondPy(unittest.TestCase):
    state = [10, 20, 30]

    def test_markov(self) -> None:
        markov = rsp.Markov()
        markov.set_state(self.state)
        np.testing.assert_array_equal(self.state, markov.get_state())


if __name__ == "__main__":
    unittest.main("respondpy.test", warnings="error")
