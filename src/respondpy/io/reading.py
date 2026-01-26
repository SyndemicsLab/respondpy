################################################################################
# File: reading.py                                                             #
# Project: respondpy                                                           #
# Created Date: 2025-11-20                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-23                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################

from pathlib import Path
from typing import Literal
import sqlite3

from respondpy.data.parameters import Parameter

# Internal Functions


def _get_states(
        db: str | Path,
        state: Literal["intervention", "behavior"]
) -> list[str]:
    """Getter for the state tables from the SQLite database.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3
            connection.
        state (str, optional): Either "intervention" or "behavior". The specific
            state to look for in the database. Defaults to "intervention".

    Raises:
        ValueError: If the state is not "intervention" or "behavior" raise an
            error. This prevents SQL injections.

    Returns:
        list[str]: List of possible state names from the table in the SQLite
            database.
    """
    stmt = f"SELECT name FROM {state} ORDER BY id"
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(stmt)
    result = [row[0] for row in cur.fetchall()]
    con.close()
    return result


def _get_state_table(
        db: str | Path,
        state: Literal["intervention", "behavior"]
) -> list[tuple[int, str]]:
    """Getter for the state tables from the SQLite database.

    Args:
        db (str, sqlite3.Connection): Path to the SQLite database OR the sqlite3
            connection.
        state (str, optional): Either "intervention" or "behavior". The specific
            state to look for in the database. Defaults to "intervention".

    Raises:
        ValueError: If the state is not "intervention" or "behavior" raise an
            error. This prevents SQL injections.

    Returns:
        list[str]: List of possible state names from the table in the SQLite
            database.
    """
    stmt = f"SELECT id, name FROM {state} ORDER BY id"
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(stmt)
    result = [(row[0], row[1]) for row in cur.fetchall()]
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
    order_clause = "CASE\n"
    for idx, v in enumerate(values):
        order_clause += f"WHEN {col_name} = \'{v}\' THEN {idx}\n"
    order_clause += f"ELSE {len(values)}\n END"
    return order_clause


def _get_initial_cohort_by_id(
        db: str | Path,
        sample_id: int = 1
) -> tuple[list, list]:
    """Get the initial cohort from the database as a numpy array.
    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
    Returns:
        tuple[list, list]: Initial cohort as a numpy array.
    """
    i_order = _get_column_order(
        "i.name", _get_states(db, state="intervention"))
    b_order = _get_column_order(
        "b.name", _get_states(db, state="behavior"))
    con = sqlite3.connect(db)
    cur = con.cursor()
    stmt = f"""
        SELECT i.name AS intervention, b.name AS behavior, count
        FROM initial_population AS ip
        INNER JOIN intervention AS i ON ip.intervention = i.id
        INNER JOIN behavior AS b ON ip.behavior = b.id
        WHERE sample = ?
        ORDER BY
        {i_order}, {b_order}
        """
    cur.execute(stmt, str(sample_id))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result


def _get_migration_by_id_and_timestep(
        db: str | Path,
        sample_id: int = 1,
        time: int = 52
) -> tuple[list, list]:
    """Get the change in population from the database as a numpy array.
    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.
    Returns:
        tuple[list, list]: Initial cohort as a numpy array.
    """
    i_order = _get_column_order(
        "i.name", _get_states(db, state="intervention"))
    b_order = _get_column_order(
        "b.name", _get_states(db, state="behavior"))
    con = sqlite3.connect(db)
    cur = con.cursor()
    stmt = f"""
        SELECT i.name AS intervention, b.name AS behavior, count
        FROM population_change AS pc
        INNER JOIN intervention AS i ON pc.intervention = i.id
        INNER JOIN behavior AS b ON pc.behavior = b.id
        WHERE sample = ? AND time = ? 
        ORDER BY
        {i_order}, {b_order}
        """
    cur.execute(stmt, (str(sample_id), str(time)))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result


def _get_intervention_trans_by_id_and_time(
        db: str | Path,
        sample_id: int = 1,
        time: int = 52
) -> tuple[list, list]:
    """Get the intervention transitions from the database as a numpy array.

    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        tuple[list, list]: Intervention transitions as a numpy array.
    """
    ii_order = _get_column_order(
        "ii.name", _get_states(db, state="intervention"))
    ni_order = _get_column_order(
        "ni.name", _get_states(db, state="intervention"))
    b_order = _get_column_order(
        "b.name", _get_states(db, state="behavior"))
    con = sqlite3.connect(db)
    cur = con.cursor()
    stmt = f"""
        SELECT ii.name AS initial_intervention, ni.name AS new_intervention, b.name AS behavior, probability
        FROM intervention_transition AS it
        INNER JOIN intervention AS ii ON it.initial_intervention = ii.id
        INNER JOIN intervention AS ni ON it.new_intervention = ni.id
        INNER JOIN behavior AS b ON it.behavior = b.id
        WHERE sample = ? AND time = ?
        ORDER BY
        {ii_order}, {ni_order}, {b_order}
        """
    cur.execute(stmt, (str(sample_id), str(time)))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result


def _get_behavior_trans_by_id_and_time(
        db: str | Path,
        sample_id: int = 1,
        time: int = 52
) -> tuple[list, list]:
    """Get the behavior transitions from the database as a numpy array.

    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        tuple[list, list]: behavior transitions as a numpy array.
    """
    i_order = _get_column_order(
        "i.name", _get_states(db, state="intervention"))
    ib_order = _get_column_order(
        "ib.name", _get_states(db, state="behavior"))
    nb_order = _get_column_order(
        "nb.name", _get_states(db, state="behavior"))
    con = sqlite3.connect(db)
    cur = con.cursor()
    stmt = f"""
        SELECT i.name AS intervention, ib.name AS initial_behavior, nb.name AS new_behavior, probability
        FROM behavior_transition AS it
        INNER JOIN intervention AS i ON it.intervention = i.id
        INNER JOIN behavior AS ib ON it.initial_behavior = ib.id
        INNER JOIN behavior AS nb ON it.new_behavior = nb.id
        WHERE sample = ? AND time = ? 
        ORDER BY
        {i_order}, {ib_order}, {nb_order}
        """
    cur.execute(stmt, (str(sample_id), str(time)))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result


def _get_od_by_id_and_time(
        db: str | Path,
        sample_id: int = 1,
        time: int = 52
) -> tuple[list, list]:
    """Get the overdose probabilities from the database as a numpy array.

    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        tuple[list, list]: behavior transitions as a numpy array.
    """
    i_order = _get_column_order(
        "i.name", _get_states(db, state="intervention"))
    b_order = _get_column_order(
        "b.name", _get_states(db, state="behavior"))
    con = sqlite3.connect(db)
    cur = con.cursor()
    stmt = f"""
        SELECT i.name AS intervention, b.name AS behavior, probability
        FROM overdose AS od
        INNER JOIN intervention AS i ON od.intervention = i.id
        INNER JOIN behavior AS b ON od.behavior = b.id
        WHERE sample = ? AND time = ?
        ORDER BY
        {i_order}, {b_order}
        """
    cur.execute(stmt, (str(sample_id), str(time)))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result


def _get_fod_by_id_and_time(
        db: str | Path,
        sample_id: int = 1,
        time: int = 52
) -> tuple[list, list]:
    """Get the fatal overdose probabilities from the database as a numpy array.

    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        tuple[list, list]: behavior transitions as a numpy array.
    """
    i_order = _get_column_order(
        "i.name", _get_states(db, state="intervention"))
    b_order = _get_column_order(
        "b.name", _get_states(db, state="behavior"))
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT i.name AS intervention, b.name AS behavior, probability
        FROM overdose_fatality AS fod
        INNER JOIN intervention AS i ON fod.intervention = i.id
        INNER JOIN behavior AS b ON fod.behavior = b.id
        WHERE sample = ? AND time = ?
        ORDER BY
        {i_order}, {b_order}
        """, (str(sample_id), str(time)))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result


def _get_bg_death_by_id_and_time(
        db: str | Path,
        sample_id: int = 1,
        time: int = 52
) -> tuple[list, list]:
    """Get the background mortality probabilities from the database as a numpy array.

    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        tuple[list, list]: behavior transitions as a numpy array.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    stmt = """
        SELECT probability
        FROM background_mortality
        WHERE sample = ? AND time = ?
        """
    cur.execute(stmt, (str(sample_id), str(time)))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result


def _get_smr_by_id_and_time(
        db: str | Path,
        sample_id: int = 1,
        time: int = 52
) -> tuple[list, list]:
    """Get the SMRs from the database as a numpy array.

    Args:
        db (str, Path): Path to the SQLite database.
        sample_id (int, optional): Sample ID to retrieve. Defaults to 1.
        time (int, optiona): Time point to retrieve. Defaults to 52.

    Returns:
        tuple[list, list]: behavior transitions as a numpy array.
    """
    i_order = _get_column_order(
        "i.name", _get_states(db, state="intervention"))
    b_order = _get_column_order(
        "b.name", _get_states(db, state="behavior"))
    con = sqlite3.connect(db)
    cur = con.cursor()
    stmt = f"""
        SELECT i.name AS intervention, b.name AS behavior, ratio
        FROM smr
        INNER JOIN intervention AS i ON smr.intervention = i.id
        INNER JOIN behavior AS b ON smr.behavior = b.id
        WHERE sample = ? AND time = ?
        ORDER BY
        {i_order}, {b_order}
        """
    cur.execute(stmt, (str(sample_id), str(time)))
    col_names = [d[0] for d in cur.description]
    result = cur.fetchall()
    con.close()
    return col_names, result

# External Functions


def get_parameter_by_id_and_time(
        param: Parameter,
        db: str | Path,
        sample_id: int,
        time: int
) -> tuple[list, list]:
    if not Path(db).is_file():
        raise FileNotFoundError(
            f"The database file was not found when attempting to retrieve parameters by id and time! File specified: {db}.")

    if param == Parameter.INITIAL_COHORT:
        return _get_initial_cohort_by_id(db, sample_id)
    if param == Parameter.MIGRATION_COHORT:
        return _get_migration_by_id_and_timestep(db, sample_id, time)
    if param == Parameter.INTERVENTION_TRANSITION_PROBABILITY:
        return _get_intervention_trans_by_id_and_time(db, sample_id, time)
    if param == Parameter.BEHAVIOR_TRANSITION_PROBABILITY:
        return _get_behavior_trans_by_id_and_time(db, sample_id, time)
    if param == Parameter.STANDARD_MORTALITY_RATIO:
        return _get_smr_by_id_and_time(db, sample_id, time)
    if param == Parameter.BACKGROUND_DEATH_PROBABILITY:
        return _get_bg_death_by_id_and_time(db, sample_id, time)
    if param == Parameter.OVERDOSE_PROBABILITY:
        return _get_od_by_id_and_time(db, sample_id, time)
    if param == Parameter.OVERDOSE_FATALITY_PROBABILITY:
        return _get_fod_by_id_and_time(db, sample_id, time)
    raise ValueError(
        f"Attempting to extract invalid parameter of value {param}!")


def get_interventions(db: str | Path) -> list[str]:
    """Get the list of interventions the describe the model.

    Args:
        db (str | Path): Path to the SQLite database.

    Returns:
        list[str]: A list of intervention names.
    """
    return _get_states(db, state="intervention")


def get_behaviors(db: str | Path) -> list[str]:
    """Get the list of behaviors the describe the model.

    Args:
        db (str | Path): Path to the SQLite database.

    Returns:
        list[str]: A list of behavior names.
    """
    return _get_states(db, state="behavior")


def get_intervention_table(db: str | Path) -> list[tuple[int, str]]:
    """Return the intervention table as a list of id, name tuples

    Args:
        db (str | Path): Path to the SQLite database.

    Returns:
        list[tuple[int, str]]: A list of tuples containing id, name interventions.
    """
    return _get_state_table(db, state="intervention")


def get_behavior_table(db: str | Path) -> list[tuple[int, str]]:
    """Return the intervention table as a list of id, name tuples

    Args:
        db (str | Path): Path to the SQLite database.

    Returns:
        list[tuple[int, str]]: A list of tuples containing id, name behaviors.
    """
    return _get_state_table(db, state="behavior")


def get_state_names(
        db: str | Path
) -> list[tuple[str, str]]:
    """Get the intervention and behavior names in a list of tuples sorted by intervention and behavior ID.

    Args:
        db (str, Path): Path to the SQLite database.
    Returns:
        list[tuple[str]]: List of tuples containing intervention, behavior combinations that form the state names.
    """
    if not Path(db).is_file():
        raise FileNotFoundError(
            f"The database file was not found when attempting to retrieve state names! File specified: {db}.")
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(
        """
        SELECT i.name AS intervention, b.name AS behavior
        FROM intervention AS i
        CROSS JOIN behavior AS b
        ORDER BY i.id, b.id
        """
    )
    result = cur.fetchall()
    con.close()
    return result


def get_cohorts(db: str | Path) -> tuple[list[str], list]:
    """Get all the cohorts from the database.

    Args:
        db (str | Path): Path to the database.

    Returns:
        tuple[list[str], list]: a tuple of the column names and then a list of the cohort details.
    """
    if not Path(db).is_file():
        raise FileNotFoundError(
            f"The database file was not found when attempting to retrieve state names! File specified: {db}.")
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM cohort;
        """
    )
    column_names = [description[0] for description in cur.description]
    result = cur.fetchall()
    con.close()
    return column_names, result
