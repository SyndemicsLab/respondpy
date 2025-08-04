from __future__ import annotations
import collections.abc
import numpy
import numpy.typing
import typing
__all__ = ['CostStamp', 'CreationStatus', 'HistoryStamp', 'LogType', 'Markov', 'ResultSets', 'Totals', 'UtilityType', 'behavior', 'calculate_life_years', 'calculate_perspectives', 'calculate_total_costs', 'create_file_logger', 'discount', 'discount_cost_stamp', 'intervention', 'kDebug', 'kError', 'kExists', 'kInfo', 'kMin', 'kMult', 'kNotCreated', 'kSuccess', 'kWarn', 'log_debug', 'log_error', 'log_info', 'log_warning', 'migration', 'mortality', 'overdose', 'stamp_costs', 'stamp_costs_over_time', 'stamp_utilities', 'stamp_utilities_over_time']
class CostStamp:
    def __init__(self) -> None:
        ...
    @property
    def fatal_overdoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @fatal_overdoses.setter
    def fatal_overdoses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def healthcare(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @healthcare.setter
    def healthcare(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def non_fatal_overdoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @non_fatal_overdoses.setter
    def non_fatal_overdoses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def pharmaceuticals(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @pharmaceuticals.setter
    def pharmaceuticals(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def treatments(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @treatments.setter
    def treatments(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
class CreationStatus:
    """
    Members:
    
      kError
    
      kSuccess
    
      kExists
    
      kNotCreated
    """
    __members__: typing.ClassVar[dict[str, CreationStatus]]  # value = {'kError': <CreationStatus.kError: -1>, 'kSuccess': <CreationStatus.kSuccess: 0>, 'kExists': <CreationStatus.kExists: 1>, 'kNotCreated': <CreationStatus.kNotCreated: 2>}
    kError: typing.ClassVar[CreationStatus]  # value = <CreationStatus.kError: -1>
    kExists: typing.ClassVar[CreationStatus]  # value = <CreationStatus.kExists: 1>
    kNotCreated: typing.ClassVar[CreationStatus]  # value = <CreationStatus.kNotCreated: 2>
    kSuccess: typing.ClassVar[CreationStatus]  # value = <CreationStatus.kSuccess: 0>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class HistoryStamp:
    def __init__(self) -> None:
        ...
    @property
    def intervention_admissions(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @intervention_admissions.setter
    def intervention_admissions(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def overdoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @overdoses.setter
    def overdoses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def state(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @state.setter
    def state(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
class LogType:
    """
    Members:
    
      kInfo
    
      kWarn
    
      kError
    
      kDebug
    """
    __members__: typing.ClassVar[dict[str, LogType]]  # value = {'kInfo': <LogType.kInfo: 0>, 'kWarn': <LogType.kWarn: 1>, 'kError': <LogType.kError: 2>, 'kDebug': <LogType.kDebug: 3>}
    kDebug: typing.ClassVar[LogType]  # value = <LogType.kDebug: 3>
    kError: typing.ClassVar[LogType]  # value = <LogType.kError: 2>
    kInfo: typing.ClassVar[LogType]  # value = <LogType.kInfo: 0>
    kWarn: typing.ClassVar[LogType]  # value = <LogType.kWarn: 1>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Markov:
    def __init__(self, log_name: str = 'console') -> None:
        ...
    def add_transition(self, arg0: tuple[..., -1, 1, 0, -1, ..., collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]]) -> None:
        ...
    def get_run_results(self) -> dict[int, HistoryStamp]:
        ...
    def get_state(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def get_transitions(self) -> list[tuple[..., -1, 1, 0, -1, ..., list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]]]:
        ...
    def run(self, arg0: typing.SupportsInt) -> None:
        ...
    def set_state(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    def set_transitions(self, arg0: collections.abc.Sequence[tuple[..., -1, 1, 0, -1, ..., collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]]]) -> None:
        ...
class ResultSets:
    def __init__(self) -> None:
        ...
    @property
    def summed_costs(self) -> list[float]:
        ...
    @summed_costs.setter
    def summed_costs(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def summed_life_years(self) -> float:
        ...
    @summed_life_years.setter
    def summed_life_years(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def summed_utility(self) -> float:
        ...
    @summed_utility.setter
    def summed_utility(self, arg0: typing.SupportsFloat) -> None:
        ...
class Totals:
    base: ResultSets
    discounted: ResultSets
    def __init__(self) -> None:
        ...
class UtilityType:
    """
    Members:
    
      kMin
    
      kMult
    """
    __members__: typing.ClassVar[dict[str, UtilityType]]  # value = {'kMin': <UtilityType.kMin: 0>, 'kMult': <UtilityType.kMult: 1>}
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
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def behavior(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Behavior Transition.
    """
def calculate_life_years(arg0: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], arg1: bool, arg2: typing.SupportsFloat) -> float:
    """
    Calculate the life years.
    """
def calculate_perspectives(arg0: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], arg1: collections.abc.Sequence[str], arg2: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], arg3: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], arg4: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], arg5: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], arg6: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], arg7: bool, arg8: typing.SupportsFloat) -> dict[str, dict[int, CostStamp]]:
    """
    Calculate the Cost Stamps for the given perspectives.
    """
def calculate_total_costs(arg0: collections.abc.Mapping[typing.SupportsInt, CostStamp]) -> list[float]:
    """
    Calculate the total costs.
    """
def create_file_logger(arg0: str, arg1: str) -> CreationStatus:
    """
    Creates a File Logger for use with RESPOND.
    """
def discount(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: typing.SupportsFloat, arg2: typing.SupportsInt, arg3: bool) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Calculates the Discount for the provided Vector given the discount rate, week, and flag to indicate if it is discrete or not.
    """
def discount_cost_stamp(arg0: CostStamp, arg1: typing.SupportsFloat, arg2: typing.SupportsInt, arg3: bool) -> None:
    """
    Apply a discount to the given cost stamp.
    """
def intervention(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Intervention Transition.
    """
def log_debug(arg0: str, arg1: str) -> None:
    """
    Logs a debug message to the log.
    """
def log_error(arg0: str, arg1: str) -> None:
    """
    Logs an error message to the log.
    """
def log_info(arg0: str, arg1: str) -> None:
    """
    Logs an info message to the log.
    """
def log_warning(arg0: str, arg1: str) -> None:
    """
    Logs a warning message to the log.
    """
def migration(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Migrating Cohort.
    """
def mortality(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Mortality Transition.
    """
def overdose(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Overdose Transition.
    """
def stamp_costs(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg2: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg3: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg4: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg5: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> CostStamp:
    """
    Build a Cost Stamp.
    """
def stamp_costs_over_time(arg0: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg2: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg3: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg4: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg5: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg6: bool, arg7: typing.SupportsFloat) -> dict[int, CostStamp]:
    """
    Stamp costs over a history time period.
    """
def stamp_utilities(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Build a Utility Stamp.
    """
def stamp_utilities_over_time(arg0: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], arg2: UtilityType, arg3: bool, arg4: typing.SupportsFloat) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Stamp utilities over a history time period.
    """
kDebug: LogType  # value = <LogType.kDebug: 3>
kError: CreationStatus  # value = <CreationStatus.kError: -1>
kExists: CreationStatus  # value = <CreationStatus.kExists: 1>
kInfo: LogType  # value = <LogType.kInfo: 0>
kMin: UtilityType  # value = <UtilityType.kMin: 0>
kMult: UtilityType  # value = <UtilityType.kMult: 1>
kNotCreated: CreationStatus  # value = <CreationStatus.kNotCreated: 2>
kSuccess: CreationStatus  # value = <CreationStatus.kSuccess: 0>
kWarn: LogType  # value = <LogType.kWarn: 1>
