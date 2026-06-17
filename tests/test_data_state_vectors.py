################################################################################
# File: test_data_state_vectors.py                                             #
# Project: respondpy                                                           #
# Created Date: 2026-06-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-17                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import pytest

import respondpy.data as rpydata


@pytest.mark.unit
def test_build_constant_state_vector() -> None:
    """Test the build_constant_state_vector function."""
    inter = ["intervention_1", "intervention_2"]
    behav = ["behavior_1", "behavior_2", "behavior_3"]
    state_vector = rpydata.build_constant_state_vector(inter, behav)
    print(state_vector)
    assert state_vector.shape == (6, 5)
    assert state_vector.select("count").to_numpy().sum() == 0
    assert all(state_vector["count"] == 0.0)
