################################################################################
# File: writing.py                                                             #
# Project: respondpy                                                           #
# Created Date: 2026-01-15                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-28                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import sqlite3
from pathlib import Path

from respondpy.data.parameters import Parameter

# Internal Functions


def _check_valid_list(l: list[tuple], tuple_items: int) -> bool:
    if len(l) == 0:
        return False
    if len(l[0]) != tuple_items:
        return False
    return True


def _connect_and_execute(data: list[tuple], db: str | Path, stmt: str) -> None:
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executemany(stmt, data)
    con.commit()
    con.close()


def _insert_overdose(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 5):
        return
    sql_stmt = "INSERT INTO overdose VALUES (?, ?, ?, ?, ?)"
    _connect_and_execute(data, db, sql_stmt)


def _insert_overdose_fatality(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 5):
        return
    sql_stmt = "INSERT INTO overdose_fatality VALUES (?, ?, ?, ?, ?)"
    _connect_and_execute(data, db, sql_stmt)


def _insert_background_mortality(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 3):
        return
    sql_stmt = "INSERT INTO background_mortality VALUES (?, ?, ?)"
    _connect_and_execute(data, db, sql_stmt)


def _insert_intervention_transition(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 6):
        return
    sql_stmt = "INSERT INTO intervention_transition VALUES (?, ?, ?, ?, ?, ?)"
    _connect_and_execute(data, db, sql_stmt)


def _insert_behavior_transition(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 6):
        return
    sql_stmt = "INSERT INTO behavior_transition VALUES (?, ?, ?, ?, ?, ?)"
    _connect_and_execute(data, db, sql_stmt)


def _insert_smr(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 5):
        return
    sql_stmt = "INSERT INTO smr VALUES (?, ?, ?, ?, ?)"
    _connect_and_execute(data, db, sql_stmt)


def _insert_sample_count(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 4):
        return
    sql_stmt = "INSERT INTO initial_population VALUES (?, ?, ?, ?)"
    print(data)
    _connect_and_execute(data, db, sql_stmt)


def _insert_migration_count(data: list[tuple], db: str | Path) -> None:
    if not _check_valid_list(data, 5):
        return
    sql_stmt = "INSERT INTO population_change VALUES (?, ?, ?, ?, ?)"
    _connect_and_execute(data, db, sql_stmt)

# External Functions


def insert_cohort(data: list, db: str | Path) -> None:
    if not _check_valid_list(data, 9):
        return
    sql_stmt = """
    INSERT INTO cohort (description, background_mortality_sample, behavior_transition_sample, initial_population_sample,intervention_transition_sample, overdose_sample, overdose_fatality_sample, population_change_sample, smr_sample) VALUES (?,?,?,?,?,?,?,?,?)
    """
    _connect_and_execute(data, db, sql_stmt)


def insert_parameter(
        data: list,
        db: str | Path,
        param: Parameter
) -> None:
    if not Path(db).is_file():
        raise FileNotFoundError(
            f"The specified database could not be found: {db}")
    if param == Parameter.INITIAL_COHORT:
        return _insert_sample_count(data, db)
    if param == Parameter.MIGRATION_COHORT:
        return _insert_migration_count(data, db)
    if param == Parameter.INTERVENTION_TRANSITION_PROBABILITY:
        return _insert_intervention_transition(data, db)
    if param == Parameter.BEHAVIOR_TRANSITION_PROBABILITY:
        return _insert_behavior_transition(data, db)
    if param == Parameter.STANDARD_MORTALITY_RATIO:
        return _insert_smr(data, db)
    if param == Parameter.BACKGROUND_DEATH_PROBABILITY:
        return _insert_background_mortality(data, db)
    if param == Parameter.OVERDOSE_PROBABILITY:
        return _insert_overdose(data, db)
    if param == Parameter.OVERDOSE_FATALITY_PROBABILITY:
        return _insert_overdose_fatality(data, db)
    raise ValueError(
        f"Attempting to insert invalid parameter of value {param}!")
