################################################################################
# File: test_markov.py                                                         #
# Project: respondpy                                                           #
# Created Date: 2026-01-06                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-06                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import pytest
import numpy as np

import respondpy as rsp


def TestMarkov():
    """Test class for the Markov binded class.
    """
    state = np.array([10, 20, 30])

    def test_state_operations(self):
        """Test the ability to set and get the state from a matrix.
        """
        m = rsp.Markov()
        m.set_state(self.state)
        np.testing.assert_array_equal(self.state, m.get_state())
