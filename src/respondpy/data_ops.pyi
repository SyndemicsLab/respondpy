"""
A submodule containing the data operations necessary for RESPOND.
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['Cost', 'CostLoader', 'DataFormatter', 'DataLoader', 'Dimension', 'History', 'OutputType', 'Totals', 'UtilityLoader', 'UtilityType', 'Writer', 'WriterType', 'create_matrix3d', 'kCost', 'kDemographicCombo', 'kFile', 'kHistory', 'kInput', 'kIntervention', 'kMin',
           'kMult', 'kOud', 'kOutput', 'kString', 'kTotals', 'kUtilities', 'mult_timed_matrix3d_by_double', 'mult_timed_matrix3d_by_matrix', 'print_matrix3d', 'print_timed_matrix3d', 'sum_timed_matrix3d', 'sum_timed_matrix3d_over_dimensions', 'vec_min_matrix3d', 'vec_mult_matrix3d']


class BaseLoader:
    def load_data_table(self, path: str, headers: bool = True) -> dict[str, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def set_config(self, config_file: str) -> None:
        ...

    def get_config(self) -> dict[str, typing.Any]:
        ...


class Cost:
    fatal_overdose_cost: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]
    healthcare_cost: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]
    non_fatal_overdose_cost: dict[int,
                                  numpy.ndarray[numpy.float64[..., ..., ...]]]
    perspective: str
    pharma_cost: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]
    treatment_cost: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]

    def __init__(self) -> None:
        ...


class CostLoader:
    def __init__(self, log_name: str = 'console') -> None:
        ...

    def get_fatal_overdose_cost(self, arg0: str) -> float:
        ...

    def get_healthcare_utilization_cost(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_non_fatal_overdose_cost(self, arg0: str) -> float:
        ...

    def get_pharmaceutical_cost(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_treatment_utilization_cost(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def load_healthcare_utilization_cost(self, arg0: str) -> dict[str, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def load_overdose_cost(self, arg0: str) -> dict[str, dict[str, float]]:
        ...

    def load_pharmaceutical_cost(self, arg0: str) -> dict[str, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def load_treatment_utilization_cost(self, arg0: str) -> dict[str, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...


class DataFormatter:
    def __init__(self) -> None:
        ...

    def extract_timesteps(self, arg0: list[int], arg1: ..., arg2: list[...], arg3: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]], arg4: bool) -> None:
        ...


class DataLoader:
    def __init__(self, log_name: str = 'console') -> None:
        ...

    def get_entering_samples(self, arg0: int) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_fatal_overdose_rates(self, arg0: int) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_initial_sample(self) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_intervention_init_rates(self) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_intervention_transition_rates(self, arg0: int) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_mortality_rates(self) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_oud_transition_rates(self) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_overdose_rates(self, arg0: int) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    @typing.overload
    def load_entering_samples(self, arg0: str, arg1: str, arg2: str) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    @typing.overload
    def load_entering_samples(self, arg0: str) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def load_fatal_overdose_rates(self, arg0: str) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def load_initial_sample(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def load_intervention_init_rates(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def load_intervention_transition_rates(self, arg0: str) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def load_mortality_rates(self, arg0: str, arg1: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def load_oud_transition_rates(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def load_overdose_rates(self, arg0: str) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def set_entering_samples(self, arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]) -> None:
        ...

    def set_fatal_overdose_rates(self, arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]) -> None:
        ...

    def set_initial_sample(self, arg0: numpy.ndarray[numpy.float64[..., ..., ...]]) -> None:
        ...

    def set_intervention_init_rates(self, arg0: numpy.ndarray[numpy.float64[..., ..., ...]]) -> None:
        ...

    def set_intervention_transition_rates(self, arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]) -> None:
        ...

    def set_mortality_rates(self, arg0: numpy.ndarray[numpy.float64[..., ..., ...]]) -> None:
        ...

    def set_oud_transition_rates(self, arg0: numpy.ndarray[numpy.float64[..., ..., ...]]) -> None:
        ...

    def set_overdose_rates(self, arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]) -> None:
        ...


class Dimension:
    """
    Members:

      kIntervention

      kOud

      kDemographicCombo
    """
    __members__: typing.ClassVar[dict[str, Dimension]
                                 # value = {'kIntervention': <Dimension.kIntervention: 0>, 'kOud': <Dimension.kOud: 1>, 'kDemographicCombo': <Dimension.kDemographicCombo: 2>}
                                 ]
    # value = <Dimension.kDemographicCombo: 2>
    kDemographicCombo: typing.ClassVar[Dimension]
    # value = <Dimension.kIntervention: 0>
    kIntervention: typing.ClassVar[Dimension]
    kOud: typing.ClassVar[Dimension]  # value = <Dimension.kOud: 1>

    def __eq__(self, other: typing.Any) -> bool:
        ...

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: int) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __ne__(self, other: typing.Any) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: int) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...


class History:
    fatal_overdose_history: dict[int,
                                 numpy.ndarray[numpy.float64[..., ..., ...]]]
    intervention_admission_history: dict[int,
                                         numpy.ndarray[numpy.float64[..., ..., ...]]]
    mortality_history: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]
    overdose_history: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]
    state_history: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]

    def __init__(self) -> None:
        ...


class OutputType:
    """
    Members:

      kString

      kFile
    """
    __members__: typing.ClassVar[dict[str, OutputType]
                                 # value = {'kString': <OutputType.kString: 0>, 'kFile': <OutputType.kFile: 1>}
                                 ]
    kFile: typing.ClassVar[OutputType]  # value = <OutputType.kFile: 1>
    kString: typing.ClassVar[OutputType]  # value = <OutputType.kString: 0>

    def __eq__(self, other: typing.Any) -> bool:
        ...

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: int) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __ne__(self, other: typing.Any) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: int) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...


class Totals:
    base_costs: list[float]
    base_life_years: float
    base_utility: float
    disc_costs: list[float]
    disc_life_years: float
    disc_utility: float

    def __init__(self) -> None:
        ...


class UtilityLoader:
    def __init__(self, log_name: str = 'console') -> None:
        ...

    def get_background_utility(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_oud_utility(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def get_setting_utility(self, arg0: str) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
        ...

    def load_background_utility(self, arg0: str) -> dict[str, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def load_oud_utility(self, arg0: str) -> dict[str, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...

    def load_setting_utility(self, arg0: str) -> dict[str, numpy.ndarray[numpy.float64[..., ..., ...]]]:
        ...


class UtilityType:
    """
    Members:

      kMin

      kMult
    """
    __members__: typing.ClassVar[dict[str, UtilityType]
                                 # value = {'kMin': <UtilityType.kMin: 0>, 'kMult': <UtilityType.kMult: 1>}
                                 ]
    kMin: typing.ClassVar[UtilityType]  # value = <UtilityType.kMin: 0>
    kMult: typing.ClassVar[UtilityType]  # value = <UtilityType.kMult: 1>

    def __eq__(self, other: typing.Any) -> bool:
        ...

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: int) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __ne__(self, other: typing.Any) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: int) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...


class Writer:
    def __init__(self, directory: str = '', log_name: str = 'console') -> None:
        ...

    def write_cost_data(self, arg0: list[Cost], arg1: str, arg2: OutputType) -> str:
        ...

    def write_history_data(self, arg0: History, arg1: str, arg2: OutputType) -> str:
        ...

    def write_input_data(self, arg0: DataLoader, arg1: str, arg2: OutputType) -> str:
        ...

    def write_totals_data(self, arg0: Totals, arg1: str, arg2: OutputType) -> str:
        ...

    def write_utility_data(self, arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]], arg1: str, arg2: OutputType) -> str:
        ...


class WriterType:
    """
    Members:

      kInput

      kOutput

      kHistory

      kCost

      kUtilities

      kTotals
    """
    __members__: typing.ClassVar[dict[str, WriterType]
                                 ]  # value = {'kInput': <WriterType.kInput: 0>, 'kOutput': <WriterType.kOutput: 1>, 'kHistory': <WriterType.kHistory: 2>, 'kCost': <WriterType.kCost: 3>, 'kUtilities': <WriterType.kUtilities: 4>, 'kTotals': <WriterType.kTotals: 5>}
    kCost: typing.ClassVar[WriterType]  # value = <WriterType.kCost: 3>
    kHistory: typing.ClassVar[WriterType]  # value = <WriterType.kHistory: 2>
    kInput: typing.ClassVar[WriterType]  # value = <WriterType.kInput: 0>
    kOutput: typing.ClassVar[WriterType]  # value = <WriterType.kOutput: 1>
    kTotals: typing.ClassVar[WriterType]  # value = <WriterType.kTotals: 5>
    # value = <WriterType.kUtilities: 4>
    kUtilities: typing.ClassVar[WriterType]

    def __eq__(self, other: typing.Any) -> bool:
        ...

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: int) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __ne__(self, other: typing.Any) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: int) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...


def create_matrix3d(arg0: int, arg1: int, arg2: int) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
    """
    A Factory Function to generate a new Eigen Matrix3d.
    """


def mult_timed_matrix3d_by_double(arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]], arg1: float) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
    """
    Multiply a TimedMatrix3d by a double.
    """


def mult_timed_matrix3d_by_matrix(arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]], arg1: numpy.ndarray[numpy.float64[..., ..., ...]]) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
    """
    Multiply a TimedMatrix3d by another Matrix3d.
    """


def print_matrix3d(arg0: numpy.ndarray[numpy.float64[..., ..., ...]], arg1: ...) -> None:
    """
    Prints an Eigen Matrix3d to the provided stream.
    """


def print_timed_matrix3d(arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]], arg1: ...) -> None:
    """
    Prints a TimedMatrix3d to the provided stream.
    """


def sum_timed_matrix3d(arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
    """
    Returns the sum of a TimedMatrix3d.
    """


def sum_timed_matrix3d_over_dimensions(arg0: dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]) -> float:
    """
    Returns the sum of all elements in a TimedMatrix3d.
    """


def vec_min_matrix3d(arg0: list[numpy.ndarray[numpy.float64[..., ..., ...]]]) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
    """
    Returns the minimum of a vector of Eigen Matrix3d.
    """


def vec_mult_matrix3d(arg0: list[numpy.ndarray[numpy.float64[..., ..., ...]]]) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
    """
    Returns the product of a vector of Eigen Matrix3d.
    """


kCost: WriterType  # value = <WriterType.kCost: 3>
kDemographicCombo: Dimension  # value = <Dimension.kDemographicCombo: 2>
kFile: OutputType  # value = <OutputType.kFile: 1>
kHistory: WriterType  # value = <WriterType.kHistory: 2>
kInput: WriterType  # value = <WriterType.kInput: 0>
kIntervention: Dimension  # value = <Dimension.kIntervention: 0>
kMin: UtilityType  # value = <UtilityType.kMin: 0>
kMult: UtilityType  # value = <UtilityType.kMult: 1>
kOud: Dimension  # value = <Dimension.kOud: 1>
kOutput: WriterType  # value = <WriterType.kOutput: 1>
kString: OutputType  # value = <OutputType.kString: 0>
kTotals: WriterType  # value = <WriterType.kTotals: 5>
kUtilities: WriterType  # value = <WriterType.kUtilities: 4>
