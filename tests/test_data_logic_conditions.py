################################################################################
# File: test_data_logic_conditions.py                                          #
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
import polars as pl

import respondpy.data as rpydata


@pytest.mark.unit
def test_verify_no_nulls_raise_error() -> None:
    df = pl.DataFrame({
        "probability": [0.1, 0.2, None]
    })

    with pytest.raises(ValueError, match="Null transition probabilities found for sample 1 and parameter ParameterType.INITIAL_COHORT"):
        rpydata.verify_no_nulls(
            df, sample_id=1, p=rpydata.ParameterType.INITIAL_COHORT
        )


@pytest.mark.unit
def test_verify_no_nulls_pass() -> None:
    df = pl.DataFrame({
        "probability": [0.1, 0.2, 0.3]
    })

    rpydata.verify_no_nulls(
        df, sample_id=1, p=rpydata.ParameterType.INITIAL_COHORT
    )
    assert True  # If no error is raised, the test passes


@pytest.mark.unit
def test_verify_no_duplicates_raise_error() -> None:
    df = pl.DataFrame({
        "state_from": ["A", "A", "B"],
        "state_to": ["B", "B", "C"],
        "probability": [0.1, 0.1, 0.2]
    })

    with pytest.raises(ValueError, match="Duplicate transition rows found for sample 1 and parameter ParameterType.INITIAL_COHORT"):
        rpydata.verify_no_duplicates(
            df,
            key_columns=["state_from", "state_to"],
            sample_id=1,
            p=rpydata.ParameterType.INITIAL_COHORT
        )


@pytest.mark.unit
def test_verify_no_duplicates_pass() -> None:
    df = pl.DataFrame({
        "state_from": ["A", "B", "C"],
        "state_to": ["B", "C", "D"],
        "probability": [0.1, 0.2, 0.3]
    })

    rpydata.verify_no_duplicates(
        df,
        key_columns=["state_from", "state_to"],
        sample_id=1,
        p=rpydata.ParameterType.INITIAL_COHORT
    )
    assert True  # If no error is raised, the test passes


@pytest.mark.unit
def validate_time_list_negative_number() -> None:
    with pytest.raises(ValueError, match="The config file contains zero or a negative number in the `parameter_change_times` list!"):
        rpydata.validate_time_list([10, -5, 20])


@pytest.mark.unit
def validate_time_list_zero() -> None:
    with pytest.raises(ValueError, match="The config file contains zero or a negative number in the `parameter_change_times` list!"):
        rpydata.validate_time_list([10, 0, 20])


@pytest.mark.unit
def validate_time_list_one_value() -> None:
    input_list = [1]
    expected_output = []
    assert rpydata.validate_time_list(input_list) == expected_output


@pytest.mark.unit
def validate_time_list_valid() -> None:
    input_list = [1, 52, 104]
    expected_output = [52, 104]
    assert rpydata.validate_time_list(input_list) == expected_output


@pytest.mark.unit
def validate_time_list_no_one() -> None:
    input_list = [52, 104]
    expected_output = [52, 104]
    assert rpydata.validate_time_list(input_list) == expected_output
