################################################################################
# File: input.py                                                               #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-16                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import sqlite3
from pathlib import Path
from typing import Literal, Annotated
from operator import itemgetter
from configparser import ConfigParser

import numpy as np
import numpy.typing as npt
import polars as pl

from .database_helpers import sort_dataframes
from .parameters import Parameter, ParameterType
from .transition_matrices import build_constant_transition, update_retention_probability, combine_dataframes
from .state_vectors import build_constant_state_vector


class Input:
    """Data access object for RESPOND SQLite and simulation configuration.

    This class resolves cohort-linked sample ids, loads raw parameter tables,
    and returns either raw rows or model-ready numpy arrays.
    """

    def __init__(
        self,
        *,
        path: str | Path | None = None,
        db_name: str = "input.db",
        conf_name: str = "sim.conf",
        db_path: str | Path | None = None,
        conf_path: str | Path | None = None
    ) -> None:
        """Create an Input data source from a base path or explicit files.

        Parameters
        ----------
        path : str or pathlib.Path, optional
            Directory containing both database and config files.
        db_name : str, default="input.db"
            Database filename used when ``path`` is provided.
        conf_name : str, default="sim.conf"
            Config filename used when ``path`` is provided.
        db_path : str or pathlib.Path, optional
            Explicit database file path.
        conf_path : str or pathlib.Path, optional
            Explicit config file path.

        Raises
        ------
        ValueError
            If required path arguments are incomplete.
        FileNotFoundError
            If database or config files do not exist.
        """
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
        """Return parsed simulation configuration."""
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
        if state in self.states:
            return self.states[state]

        stmt = f"SELECT id, name FROM {state} ORDER BY id"
        _, results = self._connect_and_fetchall(stmt)
        self.states[state] = [(row[0], row[1]) for row in results]
        return self.states[state]

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
            lzdf = pl.LazyFrame(
                vals, schema=cols, orient='row'
            ).with_columns(sample=sample_id)
        else:
            cols, vals = self._connect_and_fetchall(
                stmt, (str(sample_id), str(time)))
            lzdf = pl.LazyFrame(
                vals, schema=cols, orient='row'
            ).with_columns(
                sample=sample_id,
                time=time
            )

        return lzdf

    def _extract_values(
        self,
        param: Parameter,
        lf: pl.LazyFrame,
        *,
        n: int = 64
    ) -> Annotated[npt.NDArray[np.float64], "[m, 1] | [m, m]"]:
        """Convert extracted rows to a model-ready state vector or matrix.

        Parameters
        ----------
        param : Parameter
            Parameter descriptor controlling output shape.
        lf : polars.LazyFrame
            LazyFrame containing extracted values.
        n : int, default=64
            Number of states in the model. (Default is 64 which corresponds to 16 interventions * 4 behaviors)

        Returns
        -------
        numpy.typing.NDArray[numpy.float64]
            ``(n, 1)`` state vector or ``(n, n)`` transition matrix.

        Raises
        ------
        ValueError
            If ``param`` cannot be mapped to either shape.
        """
        val_col_name = param.get_value_column_name()
        if param.is_state_vector_operation():
            vec = lf.select(pl.col(val_col_name)).collect().to_numpy()
            return vec.reshape(n, 1)
        if param.is_transition_matrix_operation():
            return lf.select(
                pl.col(val_col_name)
            ).collect().to_numpy().reshape(n, n)
        raise ValueError(
            "Invalid parameter applied when attempting to extract parameters!")

    def _zero_invalid_transitions(
        self,
        param: Parameter,
        transition_matrix: pl.DataFrame
    ) -> pl.DataFrame:
        """Set structurally invalid transition probabilities to zero.

        For intervention transitions, behavior changes are invalid. For behavior
        transitions, intervention changes are invalid.

        Parameters
        ----------
        param : Parameter
            Parameter descriptor identifying transition type.
        transition_matrix : polars.DataFrame
            Transition rows to sanitize.

        Returns
        -------
        polars.DataFrame
            Transition dataframe with invalid rows forced to zero.
        """
        if param == ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
            m = transition_matrix.with_columns(
                pl.when(
                    pl.col("new_behavior") != pl.col("initial_behavior")
                ).then(
                    pl.lit(0.0)
                ).otherwise(
                    pl.col("probability")
                ).alias("probability")
            )
        elif param == ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
            m = transition_matrix.with_columns(
                pl.when(
                    pl.col("new_intervention") != pl.col(
                        "initial_intervention")
                ).then(
                    pl.lit(0.0)
                ).otherwise(
                    pl.col("probability")
                ).alias("probability")
            )
        else:
            m = transition_matrix
        return m

    def _get_parameter_filled(
        self,
        param: Parameter,
        sample_id: int = 1,
        time: int = 1
    ) -> pl.LazyFrame:
        """Return a complete parameter table with missing rows backfilled.

        State-vector parameters are completed from a constant state vector.
        Transition parameters are completed from a constant transition matrix,
        then normalized for retention probabilities.

        Parameters
        ----------
        param : Parameter
            Parameter descriptor to extract.
        sample_id : int, default=1
            Sample id selected from the cohort table.
        time : int, default=1
            Timestep used for time-varying parameters.

        Returns
        -------
        polars.LazyFrame
            Complete and consistently ordered parameter rows.

        Raises
        ------
        ValueError
            If required transition state columns are missing.
        """
        lf = self._select_parameter_raw(param, sample_id, time)
        if param == ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
            lf = lf.rename({"behavior": "initial_behavior"})
        elif param == ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
            lf = lf.rename({"intervention": "initial_intervention"})

        n_rows = lf.select(pl.len()).collect().item()

        n_interventions = len(self.get_interventions())
        n_behaviors = len(self.get_behaviors())
        n_states = n_interventions * n_behaviors

        complete_state_vector = (
            param.is_state_vector_operation() and n_rows == n_states
        )
        complete_transition = (
            n_rows == n_states * n_states and param in [
                ParameterType.INTERVENTION_TRANSITION_PROBABILITY, ParameterType.BEHAVIOR_TRANSITION_PROBABILITY]
        )

        if complete_state_vector:
            return sort_dataframes(
                lf,
                self._get_single_state_table("behavior"),
                self._get_single_state_table("intervention")
            )

        if complete_transition:
            return sort_dataframes(
                lf,
                self._get_single_state_table("behavior"),
                self._get_single_state_table("intervention")
            )

        if param.is_state_vector_operation():
            value_col = param.get_value_column_name()
            return combine_dataframes(
                build_constant_state_vector(
                    self.get_interventions(), self.get_behaviors(), sample_id=sample_id, time=time, value_column=value_col
                ).lazy(),
                lf,
                value_col=value_col
            )
        temp = build_constant_transition(
            self.get_interventions(),
            self.get_behaviors(),
            sample_id=sample_id,
            time=time
        )

        res = combine_dataframes(
            temp, lf, value_col=param.get_value_column_name()
        )

        init_col = param.get_initial_state_column_name()
        next_col = param.get_next_state_column_name()
        if init_col is None or next_col is None:
            raise ValueError(
                f"Parameter {param} is missing the initial or next state column names required for transition matrix operations!"
            )

        res = self._zero_invalid_transitions(param, res.collect())

        res = update_retention_probability(
            res,
            init_col,
            next_col,
            probability_column=param.get_value_column_name()
        )

        return sort_dataframes(
            res.lazy(),
            self._get_single_state_table("behavior"),
            self._get_single_state_table("intervention")
        )

    # External Functions

    def get_intervention_id_maps(self) -> dict[int, str]:
        """Return a map of intervention ids to names."""
        return dict(self._get_single_state_table(state="intervention"))

    def get_interventions(self) -> list[str]:
        """Return ordered intervention names from the database."""
        if self.interventions is None:
            self.interventions = list(map(
                itemgetter(1),
                self._get_single_state_table(state="intervention")
            ))
        return self.interventions

    def get_behavior_id_maps(self) -> dict[int, str]:
        """Return a map of behavior ids to names."""
        return dict(self._get_single_state_table(state="behavior"))

    def get_behaviors(self) -> list[str]:
        """Return ordered behavior names from the database."""
        if self.behaviors is None:
            self.behaviors = list(map(
                itemgetter(1),
                self._get_single_state_table(state="behavior")
            ))
        return self.behaviors

    def get_state_names(self) -> list[tuple[str, str]]:
        """Return ordered state-name tuples as ``(intervention, behavior)``.

        Returns
        -------
        list of tuple of str
            State label pairs sorted by intervention id then behavior id.
        """
        if "combination" in self.states:
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

    def get_cohorts(self) -> tuple[list[str], list]:
        """Return raw cohort table data.

        Returns
        -------
        tuple of (list of str, list)
            Tuple of column names and row tuples from ``cohort``.
        """
        stmt = "SELECT * FROM cohort;"
        col_names, results = self._connect_and_fetchall(stmt)
        return col_names, results

    def get_cohort_ids(self) -> list[int]:
        """Return a list of cohort ids from the cohort table."""
        col_names, results = self.get_cohorts()
        id_index = col_names.index("id")
        return [row[id_index] for row in results]

    def insert_cohorts(self, data: list) -> None:
        """Insert cohort rows into the cohort table.

        Parameters
        ----------
        data : list
            Row tuples matching cohort insert statement order.
        """
        sql_stmt = """
        INSERT INTO cohort(description, background_mortality_sample, behavior_transition_sample, initial_population_sample, intervention_transition_sample, overdose_sample, overdose_fatality_sample, population_change_sample, smr_sample) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._connect_and_executemany(data, sql_stmt)

    def select_parameter(
        self,
        param: Parameter,
        cohort_id: int = 1,
        time: int = 1,
        raw: bool = False
    ) -> np.ndarray:
        """Select parameter data for a cohort and optional timestep.

        Parameters
        ----------
        param : Parameter
            Parameter descriptor to extract.
        cohort_id : int, default=1
            Cohort id used to resolve sample ids.
        time : int, default=1
            Timestep for time-varying parameters.
        raw : bool, default=False
            When ``True``, return raw table rows as numpy values.

        Returns
        -------
        numpy.ndarray
            Raw rows or model-ready shaped numpy array.
        """
        sample_id = self._get_sample_id_for_parameter(param, cohort_id)
        if raw:
            return self._select_parameter_raw(
                param, sample_id, time).collect().to_numpy()

        return self._extract_values(
            param,
            self._get_parameter_filled(param, sample_id, time),
            n=len(self.get_state_names())
        )

    def insert_parameter(
        self,
        param: Parameter,
        data: list,
    ) -> None:
        """Insert parameter rows using parameter-specific SQL.

        Parameters
        ----------
        param : Parameter
            Parameter descriptor choosing target table and schema.
        data : list
            Row tuples matching ``param`` insert statement order.
        """
        return self._connect_and_executemany(data, param.get_insert_statement())
