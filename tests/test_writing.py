################################################################################
# File: test_writing.py                                                        #
# Project: respondpy                                                           #
# Created Date: 2026-01-16                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-28                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import sqlite3
from pathlib import Path

import pytest
import polars as pl

from respondpy import insert_parameter, Parameter, insert_cohort


@pytest.fixture(scope="module", autouse=True)
def setup(tmp_path_factory, db_schema, db_cohort_insert, db_intervention_insert, db_behavior_insert):
    """Fixture to execute before all tests to setup the dummy database

    Yields:
        _type_: _description_
    """
    temp_dir = tmp_path_factory.mktemp("test-data")
    mem_str = temp_dir / "input.db"
    conn = sqlite3.connect(mem_str)
    cursor = conn.cursor()
    cursor.executescript(db_schema)
    cursor.execute(db_cohort_insert)
    cursor.execute(db_intervention_insert)
    cursor.execute(db_behavior_insert)
    conn.commit()
    conn.close()
    return mem_str


def delete(db_file, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()
    conn.close()


class TestWriting:
    """Test Class for the file writing.py
    """

    def _count_rows(self, db_file: str | Path, table: str) -> int:
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        stmt = f"SELECT COUNT(*) FROM {table}"
        cur.execute(stmt)
        result = cur.fetchone()[0]
        con.close()
        return result

    def test_insert_initial_cohort(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2],
            "count": [100, 200, 300, 400]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.INITIAL_COHORT)

        assert self._count_rows(db_file, "initial_population") == df.height

    def test_insert_migrating_cohort(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1],
            "count": [100, 200, 300, 400]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.MIGRATION_COHORT)

        assert self._count_rows(db_file, "population_change") == df.height

    def test_insert_intervention_transition(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1, 1, 1, 1, 1],
            "behavior": [1, 2, 1, 2, 1, 2, 1, 2],
            "time": [1, 1, 1, 1, 1, 1, 1, 1],
            "initial_intervention": [1, 1, 2, 2, 1, 1, 2, 2],
            "new_intervention": [1, 1, 1, 1, 2, 2, 2, 2],
            "probability": [.25, .25, .25, .25, .25, .25, .25, .25]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.INTERVENTION_TRANSITION_PROBABILITY)

        assert self._count_rows(
            db_file, "intervention_transition") == df.height

    def test_insert_behavior_transition(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1, 1, 1, 1, 1],
            "intervention": [1, 2, 1, 2, 1, 2, 1, 2],
            "time": [1, 1, 1, 1, 1, 1, 1, 1],
            "initial_behavior": [1, 1, 2, 2, 1, 1, 2, 2],
            "new_behavior": [1, 1, 1, 1, 2, 2, 2, 2],
            "probability": [.25, .25, .25, .25, .25, .25, .25, .25]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.BEHAVIOR_TRANSITION_PROBABILITY)

        assert self._count_rows(
            db_file, "behavior_transition") == df.height

    def test_insert_smr(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1],
            "ratio": [100, 200, 300, 400]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.STANDARD_MORTALITY_RATIO)

        assert self._count_rows(db_file, "smr") == df.height

    def test_insert_background_mortality(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "sample": [1],
            "time": [1],
            "ratio": [100]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.BACKGROUND_DEATH_PROBABILITY)

        assert self._count_rows(db_file, "background_mortality") == df.height

    def test_insert_overdose(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "intervention": [1, 1, 2, 2],
            "sample": [1, 1, 1, 1],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1],
            "probability": [100, 200, 300, 400]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.OVERDOSE_PROBABILITY)

        assert self._count_rows(db_file, "overdose") == df.height

    def test_insert_fatal_overdose(self, setup):
        db_file = setup
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1],
            "probability": [100, 200, 300, 400]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.OVERDOSE_FATALITY_PROBABILITY)

        assert self._count_rows(db_file, "overdose_fatality") == df.height

    def test_insert_invalid_file(self):
        """Test the ability to get the init cohort from the database
        """
        with pytest.raises(FileNotFoundError, match="The specified database could not be found:"):
            insert_parameter([], "",
                             Parameter.OVERDOSE_FATALITY_PROBABILITY)

    def test_insert_cohort(self, setup):
        df = pl.DataFrame({
            "description": ["sample 1", "sample 2"],
            "background_mortality_sample": [1, 1],
            "behavior_transition_sample": [1, 1],
            "initial_population_sample": [1, 1],
            "intervention_transition_sample": [1, 1],
            "overdose_sample": [1, 1],
            "overdose_fatality_sample": [1, 1],
            "population_change_sample": [1, 1],
            "smr_sample": [1, 1]
        })

        insert_cohort(df.rows(), setup)
        # since a cohort is already present we +1 the height
        assert self._count_rows(setup, "cohort") == df.height+1


class TestInvalidWriting:
    """Class to test the invalid writing attempts
    """

    def _count_rows(self, db_file: str | Path, table: str) -> int:
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        stmt = f"SELECT COUNT(*) FROM {table}"
        cur.execute(stmt)
        result = cur.fetchone()[0]
        con.close()
        return result

    def test_insert_initial_cohort(self, setup):
        db_file = setup
        delete(db_file, "initial_population")
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2]
        })

        insert_parameter(df.rows(),
                         db_file, Parameter.INITIAL_COHORT)

        assert self._count_rows(db_file, "initial_population") == 0

    def test_insert_migrating_cohort(self, setup):
        db_file = setup
        delete(db_file, "population_change")
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.MIGRATION_COHORT)

        assert self._count_rows(db_file, "population_change") == 0

    def test_insert_intervention_transition(self, setup):
        db_file = setup
        delete(db_file, "intervention_transition")
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1, 1, 1, 1, 1],
            "behavior": [1, 2, 1, 2, 1, 2, 1, 2],
            "time": [1, 1, 1, 1, 1, 1, 1, 1],
            "initial_intervention": [1, 1, 2, 2, 1, 1, 2, 2],
            "new_intervention": [1, 1, 1, 1, 2, 2, 2, 2]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.INTERVENTION_TRANSITION_PROBABILITY)

        assert self._count_rows(
            db_file, "intervention_transition") == 0

    def test_insert_behavior_transition(self, setup):
        db_file = setup
        delete(db_file, "behavior_transition")
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1, 1, 1, 1, 1],
            "intervention": [1, 2, 1, 2, 1, 2, 1, 2],
            "time": [1, 1, 1, 1, 1, 1, 1, 1],
            "initial_behavior": [1, 1, 2, 2, 1, 1, 2, 2],
            "new_behavior": [1, 1, 1, 1, 2, 2, 2, 2]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.BEHAVIOR_TRANSITION_PROBABILITY)

        assert self._count_rows(
            db_file, "behavior_transition") == 0

    def test_insert_smr(self, setup):
        db_file = setup
        delete(db_file, "smr")
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.STANDARD_MORTALITY_RATIO)

        assert self._count_rows(db_file, "smr") == 0

    def test_insert_background_mortality(self, setup):
        db_file = setup
        delete(db_file, "background_mortality")
        df = pl.DataFrame({
            "sample": [1],
            "time": [1]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.BACKGROUND_DEATH_PROBABILITY)

        assert self._count_rows(db_file, "background_mortality") == 0

    def test_insert_overdose(self, setup):
        db_file = setup
        delete(db_file, "overdose")
        df = pl.DataFrame({
            "intervention": [1, 1, 2, 2],
            "sample": [1, 1, 1, 1],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.OVERDOSE_PROBABILITY)

        assert self._count_rows(db_file, "overdose") == 0

    def test_insert_fatal_overdose(self, setup):
        db_file = setup
        delete(db_file, "overdose_fatality")
        df = pl.DataFrame({
            "sample": [1, 1, 1, 1],
            "intervention": [1, 1, 2, 2],
            "behavior": [1, 2, 1, 2],
            "time": [1, 1, 1, 1]
        })
        insert_parameter(df.rows(),
                         db_file, Parameter.OVERDOSE_FATALITY_PROBABILITY)

        assert self._count_rows(db_file, "overdose_fatality") == 0
