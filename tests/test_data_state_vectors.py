################################################################################
# File: test_data_state_vectors.py                                             #
# Project: respondpy                                                           #
# Created Date: 2026-06-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import pytest

import respondpy.data as rpydata


@pytest.mark.unit
def test_build_constant_state_vector() -> None:
    """Test the build_constant_state_vector function."""
    state_vector = rpydata.build_constant_state_vector(5, 1)
    assert state_vector.shape == (5, 5)
    assert state_vector.select("probability").to_numpy().sum() == 0
    assert all(state_vector["probability"] == 0.0)
