################################################################################
# File: sqlite_eigen.py                                                        #
# Project: respondpy                                                           #
# Created Date: 2025-11-20                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2025-11-24                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025 Syndemics Lab at Boston Medical Center                    #
################################################################################
import sqlite3
import numpy as np


def _get_states_from_db(
        db: str | sqlite3.Connection,
        state: str = "intervention"
) -> list[str]:
    """Getter for the state tables from the SQLite database.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        state (str, optional): Either "intervention" or "behavior". The specific state to look for in the database. Defaults to "intervention".

    Raises:
        ValueError: If the state is not "intervention" or "behavior" raise an error. This prevents SQL injections.

    Returns:
        list[str]: List of possible state names from the table in the SQLite database.
    """
    if state not in ["intervention", "behavior"]:
        raise ValueError("State must be either 'intervention' or 'behavior'!")
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute("SELECT name FROM ? ORDER BY id", (state))
    result = [row[0] for row in cur.fetchall()]
    con.close()
    return result


def _get_column_order(
        col_name: str,
        values: list[str]
) -> str:
    """Get the SQL ORDER BY clause for a given column and list of values.

    Args:
        col_name (str): column in the SQLite table to order by.
        values (list[str]): List of values to order by.

    Returns:
        str: String representing the SQL ORDER BY clause.
    """
    order_clause = f"ORDER BY CASE {col_name}\n"
    for idx, v in enumerate(values):
        order_clause += f"WHEN {v} THEN {idx}\n"
    order_clause += f"ELSE {len(values)}\n END"
    return order_clause


def get_init_cohort_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1
) -> np.ndarray:
    """Get the initial cohort from the database as a numpy array.
    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
    Returns:
        np.ndarray: Initial cohort as a numpy array.
    """
    i_order = _get_column_order("i.name", _get_states_from_db(db))
    b_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT count
        FROM initial_population AS ip
        INNER JOIN intervention AS i ON ip.intervention = i.id
        INNER JOIN behavior AS b ON ip.behavior = b.id 
        WHERE cohort = ? 
        {i_order}, {b_order}
        """, (str(cohort_id)))
    result = np.array(cur.fetchall())
    con.close()
    return result


def get_population_change_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1,
        time: int = 52
) -> np.ndarray:
    """Get the change in population from the database as a numpy array.
    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.
    Returns:
        np.ndarray: Initial cohort as a numpy array.
    """
    i_order = _get_column_order("i.name", _get_states_from_db(db))
    b_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT count
        FROM population_change AS pc
        INNER JOIN intervention AS i ON pc.intervention = i.id
        INNER JOIN behavior AS b ON pc.behavior = b.id 
        WHERE cohort = ? AND time = ?
        {i_order}, {b_order}
        """, (str(cohort_id), str(time)))
    result = np.array(cur.fetchall())
    con.close()
    return result


def get_intervention_transitions_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1,
        time: int = 52
) -> np.ndarray:
    """Get the intervention transitions from the database as a numpy array.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        np.ndarray: Intervention transitions as a numpy array.
    """
    ii_order = _get_column_order("ii.name", _get_states_from_db(db))
    ni_order = _get_column_order("ni.name", _get_states_from_db(db))
    b_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT probability
        FROM intervention_transition AS it
        INNER JOIN intervention AS ii ON it.initial_intervention = ii.id
        INNER JOIN intervention AS ni ON it.new_intervention = ni.id
        INNER JOIN behavior AS b ON it.behavior = b.id 
        WHERE cohort = ? AND time = ?
        {ii_order}, {ni_order}, {b_order}
        """, (str(cohort_id), str(time)))
    result = np.array(cur.fetchall())
    con.close()
    return result


def get_behavior_transitions_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1,
        time: int = 52
) -> np.ndarray:
    """Get the behavior transitions from the database as a numpy array.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        np.ndarray: behavior transitions as a numpy array.
    """
    i_order = _get_column_order("i.name", _get_states_from_db(db))
    ib_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    nb_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT probability
        FROM behavior_transition AS it
        INNER JOIN intervention AS i ON it.intervention = i.id 
        INNER JOIN behavior AS ib ON it.initial_behavior = ib.id
        INNER JOIN behavior AS nb ON it.new_behavior = nb.id
        WHERE cohort = ? AND time = ?
        {i_order}, {ib_order}, {nb_order}
        """, (str(cohort_id), str(time)))
    result = np.array(cur.fetchall())
    con.close()
    return result


def get_overdose_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1,
        time: int = 52
) -> np.ndarray:
    """Get the overdose probabilities from the database as a numpy array.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        np.ndarray: behavior transitions as a numpy array.
    """
    i_order = _get_column_order("i.name", _get_states_from_db(db))
    b_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT probability
        FROM overdose AS od
        INNER JOIN intervention AS i ON od.intervention = i.id 
        INNER JOIN behavior AS b ON od.behavior = b.id
        WHERE cohort = ? AND time = ?
        {i_order}, {b_order}
        """, (str(cohort_id), str(time)))
    result = np.array(cur.fetchall())
    con.close()
    return result


def get_fatal_overdose_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1,
        time: int = 52
) -> np.ndarray:
    """Get the fatal overdose probabilities from the database as a numpy array.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        np.ndarray: behavior transitions as a numpy array.
    """
    i_order = _get_column_order("i.name", _get_states_from_db(db))
    b_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT probability
        FROM overdose_fatality AS fod
        INNER JOIN intervention AS i ON fod.intervention = i.id 
        INNER JOIN behavior AS b ON fod.behavior = b.id
        WHERE cohort = ? AND time = ?
        {i_order}, {b_order}
        """, (str(cohort_id), str(time)))
    result = np.array(cur.fetchall())
    con.close()
    return result


def get_background_mortality_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1,
        time: int = 52
) -> np.ndarray:
    """Get the background mortality probabilities from the database as a numpy array.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        np.ndarray: behavior transitions as a numpy array.
    """
    i_order = _get_column_order("i.name", _get_states_from_db(db))
    b_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT probability
        FROM background_mortality
        WHERE cohort = ? AND time = ?
        {i_order}, {b_order}
        """, (str(cohort_id), str(time)))
    result = np.array(cur.fetchall())
    con.close()
    return result


def get_smr_from_db(
        db: str | sqlite3.Connection,
        cohort_id: int = 1,
        time: int = 52
) -> np.ndarray:
    """Get the SMRs from the database as a numpy array.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3 connection.
        cohort_id (int, optional): Cohort ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        np.ndarray: behavior transitions as a numpy array.
    """
    i_order = _get_column_order("i.name", _get_states_from_db(db))
    b_order = _get_column_order(
        "b.name", _get_states_from_db(db, state="behavior"))
    con = sqlite3.connect(db) if isinstance(db, str) else db
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT ratio
        FROM smr
        INNER JOIN intervention AS i ON smr.intervention = i.id 
        INNER JOIN behavior AS b ON smr.behavior = b.id
        WHERE cohort = ? AND time = ?
        {i_order}, {b_order}
        """, (str(cohort_id), str(time)))
    result = np.array(cur.fetchall())
    con.close()
    return result
