################################################################################
# File: test_sqlite_eigen.py                                                   #
# Project: respondpy                                                           #
# Created Date: 2025-11-24                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-06                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################
import sqlite3
import numpy as np
from numpy.testing import assert_array_equal

import pytest

from data import SCHEMA, INTERVENTION_INSERTS, BEHAVIOR_INSERTS, COHORT_INSERTS, INITIAL_POPULATION_INSERTS

from respondpy.type_conversions.sqlite_eigen import (
    get_init_cohort_from_db,
    # get_population_change_from_db, get_intervention_transitions_from_db, get_behavior_transitions_from_db, get_overdose_from_db, get_fatal_overdose_from_db, get_background_mortality_from_db, get_smr_from_db
)


@pytest.fixture(autouse=True, scope="module")
def setup():
    """Fixture to execute before all tests to setup the dummy database

    Yields:
        _type_: _description_
    """
    conn = sqlite3.connect("file:mem1?mode=memory&cached=shared")
    cursor = conn.cursor()
    cursor.execute(SCHEMA)
    cursor.execute(INTERVENTION_INSERTS)
    cursor.execute(BEHAVIOR_INSERTS)
    cursor.execute(COHORT_INSERTS)
    cursor.execute(INITIAL_POPULATION_INSERTS)
    conn.commit()
    yield conn
    conn.close()


class TestSQLiteEigen:
    """Test Class for the file sqlite_eigen.py
    """

    def test_get_init_cohort_from_db(self):
        """Test the ability to get the init cohort from the database
        """
        conn = sqlite3.connect("file:mem1?mode=memory&cached=shared")
        expected = np.array([100, 150, 200, 250])
        assert_array_equal(expected, get_init_cohort_from_db(conn, 1))
        conn.close()
