################################################################################
# File: test_reading.py                                                        #
# Project: respondpy                                                           #
# Created Date: 2025-11-24                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-04                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################
import sqlite3

import pytest

from respondpy import get_parameter_by_id_and_time, get_state_names, get_cohorts, get_interventions, get_intervention_table, get_behaviors, get_behavior_table, get_sample_ids_by_table
from respondpy import Parameter


@pytest.fixture(scope="module", autouse=True)
def setup(tmp_path_factory, db_schema, db_intervention_insert, db_behavior_insert, db_cohort_insert, db_population_insert, db_migration_insert, db_intervention_transition_insert, db_behavior_transition_insert, db_smr_insert, db_bgm_insert, db_od_insert, db_fod_insert):
    """Fixture to execute before all tests to setup the dummy database

    Yields:
        _type_: _description_
    """
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "input.db"
    conn = sqlite3.connect(mem_str)
    cursor = conn.cursor()
    cursor.executescript(db_schema)
    cursor.execute(db_intervention_insert)
    cursor.execute(db_behavior_insert)
    cursor.execute(db_cohort_insert)
    cursor.execute(db_population_insert)
    cursor.execute(db_migration_insert)
    cursor.execute(db_intervention_transition_insert)
    cursor.execute(db_behavior_transition_insert)
    cursor.execute(db_smr_insert)
    cursor.execute(db_bgm_insert)
    cursor.execute(db_od_insert)
    cursor.execute(db_fod_insert)
    conn.commit()
    conn.close()
    return mem_str


@pytest.mark.unit
class TestReading:
    """Test Class for the file reading.py
    """

    def test_get_state_names(self, setup):
        """Test the ability to get the state names from the database
        """
        db_file = setup
        expected = [
            ("no_treatment", "active_injection"),
            ("no_treatment", "nonactive_injection"),
            ("buprenorphine", "active_injection"),
            ("buprenorphine", "nonactive_injection")
        ]
        assert expected == get_state_names(db_file)

    def test_get_state_names_empty(self):
        """Test that a FileNotFoundError is raised when an invalid path is passed in.
        """
        with pytest.raises(FileNotFoundError, match="The database file was not found when attempting to retrieve state names! File specified:"):
            get_state_names("")

    def test_get_initial_cohort(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["intervention", "behavior", "count"]
        expected_vals = [
            ("no_treatment", "active_injection", 100),
            ("no_treatment", "nonactive_injection", 150),
            ("buprenorphine", "active_injection", 200),
            ("buprenorphine", "nonactive_injection", 250)
        ]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.INITIAL_COHORT, db_file, 1, 0)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_migrating_cohort(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["intervention", "behavior", "count"]
        expected_vals = [
            ("no_treatment", "active_injection", 100),
            ("no_treatment", "nonactive_injection", 150),
            ("buprenorphine", "active_injection", 200),
            ("buprenorphine", "nonactive_injection", 250)
        ]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.MIGRATION_COHORT, db_file, 1, 1)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_intervention_transitions(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["initial_intervention",
                         "new_intervention", "behavior", "probability"]
        expected_vals = [
            ("no_treatment", "no_treatment", "active_injection", 0.75),
            ("no_treatment", "no_treatment", "nonactive_injection", 0.75),
            ("no_treatment", "buprenorphine", "active_injection", 0.25),
            ("no_treatment", "buprenorphine", "nonactive_injection", 0.25),
            ("buprenorphine", "no_treatment", "active_injection", 0.0),
            ("buprenorphine", "no_treatment", "nonactive_injection", 0.2),
            ("buprenorphine", "buprenorphine", "active_injection", 1.0),
            ("buprenorphine", "buprenorphine", "nonactive_injection", 0.8),
        ]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.INTERVENTION_TRANSITION_PROBABILITY, db_file, 1, 1)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_behavior_transitions(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["intervention", "initial_behavior",
                         "new_behavior", "probability"]
        expected_vals = [
            ("no_treatment", "active_injection", "active_injection", 0.75),
            ("no_treatment", "active_injection", "nonactive_injection", 0.25),
            ("no_treatment", "nonactive_injection", "active_injection", 0.0),
            ("no_treatment", "nonactive_injection", "nonactive_injection", 1.0),
            ("buprenorphine", "active_injection", "active_injection", 0.75),
            ("buprenorphine", "active_injection", "nonactive_injection", 0.25),
            ("buprenorphine", "nonactive_injection", "active_injection", 0.2),
            ("buprenorphine", "nonactive_injection", "nonactive_injection", 0.8),
        ]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.BEHAVIOR_TRANSITION_PROBABILITY, db_file, 1, 1)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_smrs(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["intervention", "behavior", "ratio"]
        expected_vals = [
            ("no_treatment", "active_injection", 2.0),
            ("no_treatment", "nonactive_injection", 2.1),
            ("buprenorphine", "active_injection", 2.2),
            ("buprenorphine", "nonactive_injection", 2.3)
        ]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.STANDARD_MORTALITY_RATIO, db_file, 1, 1)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_background_mortality(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["probability"]
        expected_vals = [(0.25,)]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.BACKGROUND_DEATH_PROBABILITY, db_file, 1, 1)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_overdose(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["intervention", "behavior", "probability"]
        expected_vals = [
            ("no_treatment", "active_injection", 0.8),
            ("no_treatment", "nonactive_injection", 0.7),
            ("buprenorphine", "active_injection", 0.6),
            ("buprenorphine", "nonactive_injection", 0.5)
        ]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.OVERDOSE_PROBABILITY, db_file, 1, 1)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_fatal_overdose(self, setup):
        """Test the ability to get the init cohort from the database
        """
        db_file = setup
        expected_cols = ["intervention", "behavior", "probability"]
        expected_vals = [
            ("no_treatment", "active_injection", 0.1),
            ("no_treatment", "nonactive_injection", 0.2),
            ("buprenorphine", "active_injection", 0.3),
            ("buprenorphine", "nonactive_injection", 0.4)
        ]
        r_cols, r_vals = get_parameter_by_id_and_time(
            Parameter.OVERDOSE_FATALITY_PROBABILITY, db_file, 1, 1)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_parameter_invalid_file(self):
        """Test the ability to get the init cohort from the database
        """
        with pytest.raises(FileNotFoundError, match="The database file was not found when attempting to retrieve parameters by id and time! File specified:"):
            get_parameter_by_id_and_time(
                Parameter.OVERDOSE_FATALITY_PROBABILITY, "", 1, 1)

    def test_get_cohorts(self, setup):
        """Test the ability to get cohorts from the database
        """
        db_file = setup
        expected_cols = ["id", "description", "background_mortality_sample", "behavior_transition_sample", "initial_population_sample",
                         "intervention_transition_sample", "overdose_sample", "overdose_fatality_sample", "population_change_sample", "smr_sample"]
        expected_vals = [(1, "Test Cohort 1", 1, 1, 1, 1, 1, 1, 1, 1)]
        r_cols, r_vals = get_cohorts(db_file)
        assert (expected_cols, expected_vals) == (r_cols, r_vals)

    def test_get_interventions(self, setup):
        db_file = setup
        expected = ["no_treatment", "buprenorphine"]
        result = get_interventions(db_file)
        assert result == expected

    def test_get_behaviors(self, setup):
        db_file = setup
        expected = ["active_injection", "nonactive_injection"]
        result = get_behaviors(db_file)
        assert result == expected

    def test_get_intervention_table(self, setup):
        db_file = setup
        expected = [(1, "no_treatment"), (2, "buprenorphine")]
        result = get_intervention_table(db_file)
        assert result == expected

    def test_get_behavior_table(self, setup):
        db_file = setup
        expected = [(1, "active_injection"), (2, "nonactive_injection")]
        result = get_behavior_table(db_file)
        assert result == expected

    def test_get_sample_ids_by_table(self, setup):
        samples = get_sample_ids_by_table(setup, "behavior_transition")
        assert samples == [1]

    def test_get_sample_ids_no_table(self, setup):
        with pytest.raises(ValueError, match="The specified table does not exist:"):
            get_sample_ids_by_table(setup, "falalalala")

    def test_get_sample_ids_sql_injection(self, setup):
        with pytest.raises(ValueError, match="The specified table does not exist:"):
            get_sample_ids_by_table(
                setup, "behavior_transition; SELECT * FROM behavior_transition;")
