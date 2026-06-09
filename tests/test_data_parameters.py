################################################################################
# File: test_data_parameters.py                                                #
# Project: respondpy                                                           #
# Created Date: 2026-06-09                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-09                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import pytest

import respondpy.data as rpydata


@pytest.mark.unit
def test_parameter_constructor_and_equality() -> None:
    """Test the Parameter constructor."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ) == rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    )


@pytest.mark.unit
def test_parameter_inequality() -> None:
    """Test the Parameter constructor."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ) != rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY
    )


@pytest.mark.unit
def test_parameter_equality_with_enum() -> None:
    """Test the Parameter constructor."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ) == rpydata.ParameterType.INITIAL_COHORT


@pytest.mark.unit
def test_parameter_inequality_with_enum() -> None:
    """Test the Parameter constructor."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ) != rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY


@pytest.mark.unit
def test_parameter_is_state_vector_operation() -> None:
    """Test the Parameter is_state_vector_operation method."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ).is_state_vector_operation() is True


@pytest.mark.unit
def test_parameter_is_not_state_vector_operation() -> None:
    """Test the Parameter is_state_vector_operation method."""
    assert rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY
    ).is_state_vector_operation() is False


@pytest.mark.unit
def test_parameter_is_transition_matrix_operation() -> None:
    """Test the Parameter is_transition_matrix_operation method."""
    assert rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY
    ).is_transition_matrix_operation() is True


@pytest.mark.unit
def test_parameter_is_not_transition_matrix_operation() -> None:
    """Test the Parameter is_transition_matrix_operation method."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ).is_transition_matrix_operation() is False


@pytest.mark.unit
@pytest.mark.parametrize(
    ("parameter_type", "expected"),
    [
        (rpydata.ParameterType.INITIAL_COHORT, "count"),
        (rpydata.ParameterType.MIGRATION_COHORT, "count"),
        (rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY, "probability"),
        (rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY, "probability"),
        (rpydata.ParameterType.OVERDOSE_PROBABILITY, "probability"),
        (rpydata.ParameterType.OVERDOSE_FATALITY_PROBABILITY, "probability"),
        (rpydata.ParameterType.BACKGROUND_DEATH_PROBABILITY, "probability"),
        (rpydata.ParameterType.STANDARD_MORTALITY_RATIO, "ratio"),
    ],
)
def test_value_column_name(
        parameter_type: rpydata.ParameterType,
        expected: str
) -> None:
    """Test that the value column names are correct."""
    assert rpydata.Parameter(
        parameter_type
    ).get_value_column_name() == expected


@pytest.mark.unit
def test_get_initial_state_column_name() -> None:
    """Test that the initial state column name in the cohort table are correct."""
    assert rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY
    ).get_initial_state_column_name() == "initial_behavior"


@pytest.mark.unit
def test_get_initial_state_column_name_for_intervention() -> None:
    """Test transition initial-state name for intervention transitions."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY
    ).get_initial_state_column_name() == "initial_intervention"


@pytest.mark.unit
def test_get_initial_state_column_name_is_none() -> None:
    """Test that the initial state column name in the cohort table are correct."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ).get_initial_state_column_name() is None


@pytest.mark.unit
def test_get_next_state_column_name() -> None:
    """Test that the new state column name in the cohort table are correct."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY
    ).get_next_state_column_name() == "new_intervention"


@pytest.mark.unit
def test_get_next_state_column_name_for_behavior() -> None:
    """Test transition next-state name for behavior transitions."""
    assert rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY
    ).get_next_state_column_name() == "new_behavior"


@pytest.mark.unit
def test_get_next_state_column_name_is_none() -> None:
    """Test that the new state column name in the cohort table are correct."""
    assert rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ).get_next_state_column_name() is None


@pytest.mark.unit
def test_parameter_repr() -> None:
    """Test repr output for debugging readability."""
    p = rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT)
    assert repr(p) == "Parameter(parameter_type=ParameterType.INITIAL_COHORT)"


@pytest.mark.unit
def test_get_parameter_type() -> None:
    """Test parameter type getter."""
    p = rpydata.Parameter(rpydata.ParameterType.OVERDOSE_PROBABILITY)
    assert p.get_parameter_type() == rpydata.ParameterType.OVERDOSE_PROBABILITY


@pytest.mark.unit
def test_parameter_equality_with_non_parameter_type() -> None:
    """Ensure equality against unrelated objects returns False."""
    p = rpydata.Parameter(rpydata.ParameterType.INITIAL_COHORT)
    assert (p == "INITIAL_COHORT") is False


@pytest.mark.unit
@pytest.mark.parametrize(
    ("parameter_type", "expected"),
    [
        (rpydata.ParameterType.INITIAL_COHORT, False),
        (rpydata.ParameterType.MIGRATION_COHORT, True),
        (rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY, True),
        (rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY, True),
        (rpydata.ParameterType.OVERDOSE_PROBABILITY, True),
        (rpydata.ParameterType.OVERDOSE_FATALITY_PROBABILITY, True),
        (rpydata.ParameterType.BACKGROUND_DEATH_PROBABILITY, True),
        (rpydata.ParameterType.STANDARD_MORTALITY_RATIO, True),
    ],
)
def test_is_time_varying(parameter_type: rpydata.ParameterType, expected: bool) -> None:
    """Test time-varying behavior for all parameter types."""
    assert rpydata.Parameter(parameter_type).is_time_varying() is expected


@pytest.mark.unit
@pytest.mark.parametrize(
    ("parameter_type", "expected"),
    [
        (rpydata.ParameterType.INITIAL_COHORT, "initial_population_sample"),
        (rpydata.ParameterType.MIGRATION_COHORT, "population_change_sample"),
        (rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY,
         "intervention_transition_sample"),
        (rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY,
         "behavior_transition_sample"),
        (rpydata.ParameterType.OVERDOSE_PROBABILITY, "overdose_sample"),
        (rpydata.ParameterType.OVERDOSE_FATALITY_PROBABILITY,
         "overdose_fatality_sample"),
        (rpydata.ParameterType.STANDARD_MORTALITY_RATIO, "smr_sample"),
        (rpydata.ParameterType.BACKGROUND_DEATH_PROBABILITY,
         "background_mortality_sample"),
    ],
)
def test_get_cohort_column_name(parameter_type: rpydata.ParameterType, expected: str) -> None:
    """Test cohort sample column mapping for each parameter type."""
    assert rpydata.Parameter(
        parameter_type).get_cohort_column_name() == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    ("parameter_type", "expected"),
    [
        (rpydata.ParameterType.INITIAL_COHORT,
         "INSERT INTO initial_population VALUES (?, ?, ?, ?)"),
        (rpydata.ParameterType.MIGRATION_COHORT,
         "INSERT INTO population_change VALUES (?, ?, ?, ?, ?)"),
        (rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY,
         "INSERT INTO intervention_transition VALUES (?, ?, ?, ?, ?, ?)"),
        (rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY,
         "INSERT INTO behavior_transition VALUES (?, ?, ?, ?, ?, ?)"),
        (rpydata.ParameterType.OVERDOSE_PROBABILITY,
         "INSERT INTO overdose VALUES (?, ?, ?, ?, ?)"),
        (rpydata.ParameterType.OVERDOSE_FATALITY_PROBABILITY,
         "INSERT INTO overdose_fatality VALUES (?, ?, ?, ?, ?)"),
        (rpydata.ParameterType.BACKGROUND_DEATH_PROBABILITY,
         "INSERT INTO background_mortality VALUES (?, ?, ?)"),
        (rpydata.ParameterType.STANDARD_MORTALITY_RATIO,
         "INSERT INTO smr VALUES (?, ?, ?, ?, ?)"),
    ],
)
def test_get_insert_statement(parameter_type: rpydata.ParameterType, expected: str) -> None:
    """Test insert statement mapping for each parameter type."""
    assert rpydata.Parameter(parameter_type).get_insert_statement() == expected


@pytest.mark.unit
def test_get_select_statement_initial_cohort() -> None:
    """Test select statement shape for initial cohort parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.INITIAL_COHORT
    ).get_select_statement(["none", "methadone"], ["stable", "active"])
    assert "FROM initial_population" in sql
    assert "WHERE sample = ?" in sql
    assert "WHEN i.name = 'none' THEN 0" in sql
    assert "WHEN b.name = 'active' THEN 1" in sql


@pytest.mark.unit
def test_get_select_statement_migration_cohort() -> None:
    """Test select statement shape for migration cohort parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.MIGRATION_COHORT
    ).get_select_statement(["none"], ["stable"])
    assert "FROM population_change" in sql
    assert "WHERE sample = ? AND time = ?" in sql


@pytest.mark.unit
def test_get_select_statement_intervention_transition() -> None:
    """Test select statement shape for intervention transition parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.INTERVENTION_TRANSITION_PROBABILITY
    ).get_select_statement(["none", "methadone"], ["stable", "active"])
    assert "FROM intervention_transition" in sql
    assert "ii.name AS initial_intervention" in sql
    assert "ni.name AS new_intervention" in sql


@pytest.mark.unit
def test_get_select_statement_behavior_transition() -> None:
    """Test select statement shape for behavior transition parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.BEHAVIOR_TRANSITION_PROBABILITY
    ).get_select_statement(["none", "methadone"], ["stable", "active"])
    assert "FROM behavior_transition" in sql
    assert "ib.name AS initial_behavior" in sql
    assert "nb.name AS new_behavior" in sql


@pytest.mark.unit
def test_get_select_statement_overdose_fatality() -> None:
    """Test select statement shape for overdose fatality parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.OVERDOSE_FATALITY_PROBABILITY
    ).get_select_statement(["none"], ["stable"])
    assert "FROM overdose_fatality" in sql
    assert "probability" in sql


@pytest.mark.unit
def test_get_select_statement_overdose_probability() -> None:
    """Test select statement shape for overdose probability parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.OVERDOSE_PROBABILITY
    ).get_select_statement(["none"], ["stable"])
    assert "FROM overdose AS od" in sql
    assert "probability" in sql


@pytest.mark.unit
def test_get_select_statement_background_death() -> None:
    """Test select statement shape for background death parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.BACKGROUND_DEATH_PROBABILITY
    ).get_select_statement(["none"], ["stable"])
    assert "FROM background_mortality" in sql
    assert "WHERE sample = ? AND time = ?" in sql


@pytest.mark.unit
def test_get_select_statement_standard_mortality_ratio() -> None:
    """Test select statement shape for standard mortality ratio parameters."""
    sql = rpydata.Parameter(
        rpydata.ParameterType.STANDARD_MORTALITY_RATIO
    ).get_select_statement(["none"], ["stable"])
    assert "FROM smr" in sql
    assert "ratio" in sql


@pytest.mark.unit
def test_get_value_column_name_invalid_type_raises() -> None:
    """Test invalid parameter type handling for value-column lookup."""
    p = rpydata.Parameter("invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="not implemented"):
        p.get_value_column_name()


@pytest.mark.unit
def test_get_cohort_column_name_invalid_type_raises() -> None:
    """Test invalid parameter type handling for cohort-column lookup."""
    p = rpydata.Parameter("invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="not implemented"):
        p.get_cohort_column_name()


@pytest.mark.unit
def test_get_insert_statement_invalid_type_raises() -> None:
    """Test invalid parameter type handling for insert statement generation."""
    p = rpydata.Parameter("invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="not implemented"):
        p.get_insert_statement()


@pytest.mark.unit
def test_get_select_statement_invalid_type_raises() -> None:
    """Test invalid parameter type handling for select statement generation."""
    p = rpydata.Parameter("invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="only implemented"):
        p.get_select_statement(["none"], ["stable"])
