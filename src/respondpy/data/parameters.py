################################################################################
# File: parameters.py                                                          #
# Project: respondpy                                                           #
# Created Date: 2026-01-15                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-10                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

from enum import Enum

from .database_helpers import get_column_order


class ParameterType(Enum):
    """Supported parameter families used in RESPOND."""

    INITIAL_COHORT = 1
    MIGRATION_COHORT = 2
    INTERVENTION_TRANSITION_PROBABILITY = 3
    BEHAVIOR_TRANSITION_PROBABILITY = 4
    OVERDOSE_PROBABILITY = 5
    OVERDOSE_FATALITY_PROBABILITY = 6
    BACKGROUND_DEATH_PROBABILITY = 7
    STANDARD_MORTALITY_RATIO = 8


class Parameter():
    """Typed wrapper around ParameterType with SQL and schema helpers."""

    def __init__(
            self,
            parameter_type: ParameterType
    ) -> None:
        """Create a parameter descriptor.

        :param parameter_type: Enumerated parameter family.
        """
        self.__parameter_type = parameter_type

    def __eq__(self, other) -> bool:
        if isinstance(other, Parameter):
            return self.__parameter_type == other.get_parameter_type()
        if isinstance(other, ParameterType):
            return self.__parameter_type == other
        return False

    def __repr__(self) -> str:
        return f"Parameter(parameter_type={self.__parameter_type})"

    def get_parameter_type(self) -> ParameterType:
        """Return the wrapped parameter type."""
        return self.__parameter_type

    def is_time_varying(self) -> bool:
        """Return whether this parameter is indexed by timestep."""
        if self.__parameter_type == ParameterType.INITIAL_COHORT:
            return False
        return True

    def is_transition_matrix_operation(self) -> bool:
        """Return whether this parameter maps to transition-matrix data."""
        if self.__parameter_type in [ParameterType.INTERVENTION_TRANSITION_PROBABILITY, ParameterType.BEHAVIOR_TRANSITION_PROBABILITY]:
            return True
        return False

    def is_state_vector_operation(self) -> bool:
        """Return whether this parameter maps to state-vector data."""
        return not self.is_transition_matrix_operation()

    def get_value_column_name(self) -> str:
        """Return the numeric value column name used for this parameter.

        :returns: One of ``count``, ``probability``, or ``ratio``.
        :raises ValueError: If the parameter type is not implemented.
        """
        match self.__parameter_type:
            case ParameterType.STANDARD_MORTALITY_RATIO:
                return "ratio"
            case ParameterType.BACKGROUND_DEATH_PROBABILITY | ParameterType.OVERDOSE_PROBABILITY | ParameterType.OVERDOSE_FATALITY_PROBABILITY:
                return "probability"
            case ParameterType.INTERVENTION_TRANSITION_PROBABILITY | ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
                return "probability"
            case ParameterType.INITIAL_COHORT | ParameterType.MIGRATION_COHORT:
                return "count"
            case _:
                raise ValueError(
                    f"ParameterType value supplied is not implemented in the cohort table! ParameterType: {self.__parameter_type}."
                )

    def get_initial_state_column_name(self) -> str | None:
        """Return the origin-state column name for transition parameters.

        :returns: Origin-state column name, or ``None`` for non-transition
            parameters.
        """
        match self.__parameter_type:
            case ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
                return "initial_intervention"
            case ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
                return "initial_behavior"
            case _:
                return None

    def get_next_state_column_name(self) -> str | None:
        """Return the destination-state column name for transition parameters.

        :returns: Destination-state column name, or ``None`` for non-transition
            parameters.
        """
        match self.__parameter_type:
            case ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
                return "new_intervention"
            case ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
                return "new_behavior"
            case _:
                return None

    def get_cohort_column_name(self) -> str:
        """Return cohort-table sample column used by this parameter.

        :returns: Column name in the ``cohort`` table.
        :raises ValueError: If the parameter type is not implemented.
        """
        match self.__parameter_type:
            case ParameterType.INITIAL_COHORT:
                return "initial_population_sample"
            case ParameterType.MIGRATION_COHORT:
                return "population_change_sample"
            case ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
                return "intervention_transition_sample"
            case ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
                return "behavior_transition_sample"
            case ParameterType.OVERDOSE_PROBABILITY:
                return "overdose_sample"
            case ParameterType.OVERDOSE_FATALITY_PROBABILITY:
                return "overdose_fatality_sample"
            case ParameterType.STANDARD_MORTALITY_RATIO:
                return "smr_sample"
            case ParameterType.BACKGROUND_DEATH_PROBABILITY:
                return "background_mortality_sample"
            case _:
                raise ValueError(
                    f"ParameterType value supplied is not implemented in the cohort table! ParameterType: {self.__parameter_type}."
                )

    def get_insert_statement(self) -> str:
        """Return the INSERT SQL template for this parameter table.

        :returns: Parameter-specific SQL INSERT statement.
        :raises ValueError: If the parameter type is not implemented.
        """
        match self.__parameter_type:
            case ParameterType.INITIAL_COHORT:
                return "INSERT INTO initial_population VALUES (?, ?, ?, ?)"
            case ParameterType.MIGRATION_COHORT:
                return "INSERT INTO population_change VALUES (?, ?, ?, ?, ?)"
            case ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
                return "INSERT INTO intervention_transition VALUES (?, ?, ?, ?, ?, ?)"
            case ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
                return "INSERT INTO behavior_transition VALUES (?, ?, ?, ?, ?, ?)"
            case ParameterType.OVERDOSE_PROBABILITY:
                return "INSERT INTO overdose VALUES (?, ?, ?, ?, ?)"
            case ParameterType.OVERDOSE_FATALITY_PROBABILITY:
                return "INSERT INTO overdose_fatality VALUES (?, ?, ?, ?, ?)"
            case ParameterType.BACKGROUND_DEATH_PROBABILITY:
                return "INSERT INTO background_mortality VALUES (?, ?, ?)"
            case ParameterType.STANDARD_MORTALITY_RATIO:
                return "INSERT INTO smr VALUES (?, ?, ?, ?, ?)"
            case _:
                raise ValueError(
                    f"ParameterType value supplied is not implemented in the cohort table! ParameterType: {self.__parameter_type}."
                )

    def get_select_statement(
            self, interventions: list[str], behaviors: list[str]
    ) -> str:
        """Return parameter-specific SELECT SQL with deterministic ordering.

        :param interventions: Ordered intervention names used in ``ORDER BY``.
        :param behaviors: Ordered behavior names used in ``ORDER BY``.
        :returns: SQL query string for parameter extraction.
        :raises ValueError: If SELECT generation is not implemented.
        """
        match self.__parameter_type:
            case ParameterType.INITIAL_COHORT:
                return f"""
                        SELECT i.name AS intervention, b.name AS behavior, count
                        FROM initial_population AS ip
                        INNER JOIN intervention AS i ON ip.intervention = i.id
                        INNER JOIN behavior AS b ON ip.behavior = b.id
                        WHERE sample = ?
                        ORDER BY
                        {get_column_order("i.name",  interventions)}, {get_column_order("b.name", behaviors)}
                        """
            case ParameterType.MIGRATION_COHORT:
                return f"""
                        SELECT i.name AS intervention, b.name AS behavior, count
                        FROM population_change AS pc
                        INNER JOIN intervention AS i ON pc.intervention = i.id
                        INNER JOIN behavior AS b ON pc.behavior = b.id
                        WHERE sample = ? AND time = ? 
                        ORDER BY
                        {get_column_order("i.name",  interventions)}, {get_column_order("b.name",  behaviors)}
                        """
            case ParameterType.INTERVENTION_TRANSITION_PROBABILITY:
                return f"""
                        SELECT ii.name AS initial_intervention, ni.name AS new_intervention, b.name AS behavior, probability
                        FROM intervention_transition AS it
                        INNER JOIN intervention AS ii ON it.initial_intervention = ii.id
                        INNER JOIN intervention AS ni ON it.new_intervention = ni.id
                        INNER JOIN behavior AS b ON it.behavior = b.id
                        WHERE sample = ? AND time = ?
                        ORDER BY
                        {get_column_order("ii.name",  interventions)}, {get_column_order("ni.name",  interventions)}, {get_column_order("b.name",  behaviors)}
                        """
            case ParameterType.BEHAVIOR_TRANSITION_PROBABILITY:
                return f"""
                        SELECT i.name AS intervention, ib.name AS initial_behavior, nb.name AS new_behavior, probability
                        FROM behavior_transition AS it
                        INNER JOIN intervention AS i ON it.intervention = i.id
                        INNER JOIN behavior AS ib ON it.initial_behavior = ib.id
                        INNER JOIN behavior AS nb ON it.new_behavior = nb.id
                        WHERE sample = ? AND time = ? 
                        ORDER BY
                        {get_column_order("i.name",  interventions)},{get_column_order("ib.name",  behaviors)},
                        {get_column_order("nb.name",  behaviors)}
                        """
            case ParameterType.OVERDOSE_FATALITY_PROBABILITY:
                return f"""
                        SELECT i.name AS intervention, b.name AS behavior, probability
                        FROM overdose_fatality AS fod
                        INNER JOIN intervention AS i ON fod.intervention = i.id
                        INNER JOIN behavior AS b ON fod.behavior = b.id
                        WHERE sample = ? AND time = ?
                        ORDER BY
                        {get_column_order("i.name",  interventions)}, {get_column_order("b.name",  behaviors)}
                        """
            case ParameterType.OVERDOSE_PROBABILITY:
                return f"""
                        SELECT i.name AS intervention, b.name AS behavior, probability
                        FROM overdose AS od
                        INNER JOIN intervention AS i ON od.intervention = i.id
                        INNER JOIN behavior AS b ON od.behavior = b.id
                        WHERE sample = ? AND time = ?
                        ORDER BY
                        {get_column_order("i.name",  interventions)}, {get_column_order("b.name",  behaviors)}
                        """
            case ParameterType.BACKGROUND_DEATH_PROBABILITY:
                return """
                        SELECT probability
                        FROM background_mortality
                        WHERE sample = ? AND time = ?
                        """
            case ParameterType.STANDARD_MORTALITY_RATIO:
                return f"""
                        SELECT i.name AS intervention, b.name AS behavior, ratio
                        FROM smr
                        INNER JOIN intervention AS i ON smr.intervention = i.id
                        INNER JOIN behavior AS b ON smr.behavior = b.id
                        WHERE sample = ? AND time = ?
                        ORDER BY
                        {get_column_order("i.name",  interventions)}, {get_column_order("b.name",  behaviors)}
                        """
            case _:
                raise ValueError(
                    f"Select statement generation is only implemented for transition probability parameters! ParameterType: {self.__parameter_type}."
                )
