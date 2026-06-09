################################################################################
# File: input.py                                                               #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import sqlite3
from pathlib import Path
from typing import Literal
from operator import itemgetter
from configparser import ConfigParser

import numpy as np
import polars as pl

from .database_helpers import sort_dataframes
from .parameters import Parameter, ParameterType
from .transition_matrices import build_constant_transition, update_retention_probability
from .state_vectors import build_constant_state_vector


class Input:
    def __init__(
        self,
        *,
        path: str | Path | None = None,
        db_name: str = "input.db",
        conf_name: str = "sim.conf",
        db_path: str | Path | None = None,
        conf_path: str | Path | None = None
    ) -> None:
        if path is not None:
            if isinstance(path, str):
                path = Path(path)
            self._db_path = path / db_name
            self._conf_path = path / conf_name
        elif db_path is not None and conf_path is not None:
            if isinstance(db_path, str):
                db_path = Path(db_path)
            if isinstance(conf_path, str):
                conf_path = Path(conf_path)
            self._db_path = db_path
            self._conf_path = conf_path
        else:
            raise ValueError(
                "Must provide either a path or both a db_path and conf_path!"
            )

        if not self._db_path.exists():
            raise FileNotFoundError(
                f"Database file not found at {self._db_path}!")
        if not self._conf_path.exists():
            raise FileNotFoundError(
                f"Config file not found at {self._conf_path}!")

        self._db_path = db_path
        self._connection = sqlite3.connect(str(self._db_path))

        self._config = ConfigParser()
        self._config.read(self._conf_path)

        self.states: dict[str, list] = {}
        self.interventions: list[str] | None = None
        self.behaviors: list[str] | None = None

    def __repr__(self) -> str:
        return f"Input(db_path={self._db_path}, conf_path={self._conf_path})"

    @property
    def config(self) -> ConfigParser:
        return self._config

    # Helper Functions for Database Operations

    def _get_connection(self) -> sqlite3.Connection:
        if not self._connection:
            raise ConnectionError("No database connection established.")
        return self._connection

    def _check_valid_list(self, l: list[tuple], tuple_items: int) -> bool:
        if len(l) == 0:
            return False
        if len(l[0]) != tuple_items:
            return False
        return True

    def _connect_and_executemany(self, data: list[tuple], stmt: str) -> None:
        n_question_marks = stmt.count("?")
        if not self._check_valid_list(data, n_question_marks):
            raise ValueError(
                f"Data provided does not match the expected format for the SQL statement! Expected list of tuples with {n_question_marks} items each. Provided data: {data}"
            )
        con = self._get_connection()
        cur = con.cursor()
        cur.executemany(stmt, data)
        con.commit()

    def _connect_and_fetchall(
        self,
        stmt: str,
        params: tuple = ()
    ) -> tuple[list, list[tuple]]:
        con = self._get_connection()
        cur = con.cursor()
        cur.execute(stmt, params)
        col_names = [d[0] for d in cur.description]
        return col_names, cur.fetchall()

    # Helper Functions for Retrieving Data from Database

    def _get_single_state_table(
            self,
            state: Literal["intervention", "behavior"]
    ) -> list[tuple[int, str]]:
        if self.states[state]:
            return self.states[state]

        stmt = f"SELECT id, name FROM {state} ORDER BY id"
        _, results = self._connect_and_fetchall(stmt)
        self.states[state] = [(row[0], row[1]) for row in results]
        return self.states[state]

    def _get_state_names(self) -> list[tuple[str, str]]:
        """Get the intervention and behavior names in a list of tuples sorted by intervention and behavior ID.

        Args:
        Returns:
            list[tuple[str]]: List of tuples containing intervention, behavior combinations that form the state names.
        """
        if self.states["combination"]:
            return self.states["combination"]

        stmt = """
            SELECT i.name AS intervention, b.name AS behavior
            FROM intervention AS i
            CROSS JOIN behavior AS b
            ORDER BY i.id, b.id
            """

        _, results = self._connect_and_fetchall(stmt)
        self.states["combination"] = [(row[0], row[1]) for row in results]
        return self.states["combination"]

    def _get_sample_ids_by_table(
            self,
            table_name: str
    ) -> list[int]:

        con = self._get_connection()
        cur = con.cursor()

        # Check 2 things:
        #   1. Does the table exist
        #   2. Is the table_name a valid SQL string (i.e. prevent SQL injection
        #       later)
        cur.execute("""
            SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?
        """, (table_name,))
        if cur.fetchone()[0] != 1:
            raise ValueError(
                f"The specified table does not exist: {table_name}")

        # Be very careful here, this works and isn't gonna get SQL Injection attacked because we verify the table_name in the check above.
        stmt = f"SELECT DISTINCT sample FROM {table_name}"
        cur.execute(stmt)
        result = [row[0] for row in cur.fetchall()]
        return result

    def _get_sample_id_for_parameter(
            self,
            param: Parameter,
            cohort_id: int = 1
    ) -> int:
        col_name = param.get_cohort_column_name()
        stmt = f"SELECT {col_name} FROM cohort WHERE id = ?"
        _, result = self._connect_and_fetchall(stmt, (str(cohort_id),))
        if len(result) == 0 or len(result[0]) == 0:
            raise ValueError(
                f"No sample ID found for parameter {param} and cohort ID {cohort_id}!"
            )
        return result[0][0]

    def _select_parameter_raw(
        self,
        param: Parameter,
        sample_id: int = 1,
        time: int = 1
    ) -> pl.LazyFrame:
        stmt = param.get_select_statement(
            self.get_interventions(),
            self.get_behaviors()
        )
        if not param.is_time_varying():
            cols, vals = self._connect_and_fetchall(
                stmt, (str(sample_id),))
        else:
            cols, vals = self._connect_and_fetchall(
                stmt, (str(sample_id), str(time)))

        return pl.LazyFrame(vals, schema=cols, orient='row')

    def _combine_dataframes(
            self,
            df1: pl.LazyFrame,
            df2: pl.LazyFrame,
            *,
            join_cols: list[str] | None = None,
            value_col: str = "probability"
    ) -> pl.LazyFrame:
        if join_cols is None:
            join_cols = ["intervention", "behavior"]
        joined_lf = df1.join(df2, on=join_cols, how="left", suffix="_new")
        collapsed_df = joined_lf.with_columns(
            pl.when(
                pl.col(f"{value_col}_new").is_null()
            ).then(
                pl.col(value_col)
            ).otherwise(
                pl.col(f"{value_col}_new")
            ).alias(value_col)
        ).select(pl.col(df1.columns))
        return collapsed_df

    def _extract_values(
        self,
        param: Parameter,
        lf: pl.LazyFrame,
        *,
        n: int = 64  # 16 interventions * 4 behaviors
    ) -> np.ndarray:
        """Helper function to convert the dataframe rows to a numpy array reshaped into either a numpy state vector [n x 1] or transition matrix [n x n].

        Args:
            p (ParameterType): The parameter we are extracting data for
            results (pl.LazyFrame): The dataframe rows
            n (int, optional): The number of states in the state vector. Defaults to 64, assuming 16 interventions and 4 behaviors.

        Raises:
            ValueError: Invalid parameter provided.

        Returns:
            np.ndarray: A numpy matrix of either [n x 1] or [n x n]
        """
        val_col_name = param.get_value_column_name()
        if param.is_state_vector_operation():
            vec = lf.select(pl.col(val_col_name)).collect().to_numpy()
            if param == ParameterType.BACKGROUND_DEATH_PROBABILITY:
                return np.repeat(vec, n).reshape(n, 1)
            return vec.reshape(n, 1)
        if param.is_transition_matrix_operation():
            return lf.select(
                pl.col(val_col_name)
            ).collect().to_numpy().reshape(n, n)
        raise ValueError(
            "Invalid parameter applied when attempting to extract parameters!")

    def _get_parameter_filled(
        self,
        param: Parameter,
        sample_id: int = 1,
        time: int = 1
    ) -> pl.LazyFrame:
        """Helper function used to extract transitions from the database based on the cohort sample and the corresponding sample IDs.

        Args:
            p (ParameterType): The parameter to extract.
            db (str | Path): The string or Path object to the database.
            sample_ids (pl.DataFrame): The cohort sample containing the sample IDs.
            time (int | None): The timestep we are using to extract the transition. None is only valid when the initial cohort is being extracted.

        Raises:
            ValueError: Unimplemented Enum value.

        Returns:
            np.ndarray: The transition value as a numpy array.
        """
        lf = self._select_parameter_raw(param, sample_id, time)
        n_rows = lf.select(pl.len()).collect().item()

        n_interventions = len(self.get_interventions())
        n_behaviors = len(self.get_behaviors())
        n_states = n_interventions * n_behaviors

        complete_state_vector = (
            param.is_state_vector_operation() and n_rows == n_states
        )
        complete_intervention_transition = (
            n_rows == n_states * n_interventions and
            param == ParameterType.INTERVENTION_TRANSITION_PROBABILITY
        )
        complete_behavior_transition = (
            n_rows == n_states * n_behaviors and
            param == ParameterType.BEHAVIOR_TRANSITION_PROBABILITY
        )

        if complete_state_vector or complete_behavior_transition or complete_intervention_transition:
            return lf

        if param.is_state_vector_operation():
            return self._combine_dataframes(
                build_constant_state_vector(
                    n_interventions, n_behaviors, sample_id=sample_id, time=time
                ).lazy(),
                lf, value_col=param.get_value_column_name()
            )

        res = self._combine_dataframes(
            build_constant_transition(
                param.get_parameter_type(),
                n_interventions,
                n_behaviors,
                sample_id=sample_id,
                time=time
            ).lazy(),
            lf, value_col=param.get_value_column_name())

        init_col = param.get_initial_state_column_name()
        next_col = param.get_next_state_column_name()
        if init_col is None or next_col is None:
            raise ValueError(
                f"Parameter {param} is missing the initial or next state column names required for transition matrix operations!"
            )

        res = update_retention_probability(
            res.collect(),
            init_col,
            next_col,
            probability_column=param.get_value_column_name()
        )

        return sort_dataframes(
            lf,
            self._get_single_state_table("intervention"),
            self._get_single_state_table("behavior")
        )

    # External Functions

    def get_interventions(self) -> list[str]:
        if self.interventions is None:
            self.interventions = list(map(
                itemgetter(1),
                self._get_single_state_table(state="intervention")
            ))
        return self.interventions

    def get_behaviors(self) -> list[str]:
        if self.behaviors is None:
            self.behaviors = list(map(
                itemgetter(1),
                self._get_single_state_table(state="behavior")
            ))
        return self.behaviors

    def insert_cohorts(self, data: list) -> None:
        sql_stmt = """
        INSERT INTO cohort (description, background_mortality_sample, behavior_transition_sample, initial_population_sample,intervention_transition_sample, overdose_sample, overdose_fatality_sample, population_change_sample, smr_sample) VALUES (?,?,?,?,?,?,?,?,?)
        """
        self._connect_and_executemany(data, sql_stmt)

    def get_cohorts(self) -> tuple[list[str], list]:
        stmt = "SELECT * FROM cohort;"
        col_names, results = self._connect_and_fetchall(stmt)
        return col_names, results

    def insert_parameter(
        self,
        param: Parameter,
        data: list,
    ) -> None:
        return self._connect_and_executemany(data, param.get_insert_statement())

    def select_parameter(
        self,
        param: Parameter,
        cohort_id: int = 1,
        time: int = 1,
        raw: bool = False
    ) -> np.ndarray:
        sample_id = self._get_sample_id_for_parameter(param, cohort_id)
        if raw:
            return self._select_parameter_raw(
                param, sample_id, time).collect().to_numpy()

        return self._extract_values(
            param,
            self._get_parameter_filled(param, sample_id, time),
            n=len(self._get_state_names())
        )
