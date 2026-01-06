from __future__ import annotations
import collections.abc
import typing

import numpy
import numpy.typing
__all__ = ['CostStamp', 'CreationStatus', 'HistoryStamp', 'LogType', 'Markov', 'ResultSets', 'Totals', 'UtilityType', 'behavior', 'calculate_life_years', 'calculate_perspectives', 'calculate_total_costs', 'create_file_logger', 'discount', 'discount_cost_stamp', 'intervention',
           'kDebug', 'kError', 'kExists', 'kInfo', 'kMin', 'kMult', 'kNotCreated', 'kSuccess', 'kWarn', 'log_debug', 'log_error', 'log_info', 'log_warning', 'migration', 'mortality', 'overdose', 'stamp_costs', 'stamp_costs_over_time', 'stamp_utilities', 'stamp_utilities_over_time']


class CostStamp:
    """
    Class grouping together matrices containing cost information.

    Members:
      healthcare
      non_fatal_overdoses
      fatal_overdoses
      pharmaceuticals
      treatments
    """

    def __init__(self) -> None:
        ...

    @property
    def fatal_overdoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing fatal overdose cost information."
    @fatal_overdoses.setter
    def fatal_overdoses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...

    @property
    def healthcare(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing healthcare cost information."
    @healthcare.setter
    def healthcare(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...

    @property
    def non_fatal_overdoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing non-fatal overdose cost information."
    @non_fatal_overdoses.setter
    def non_fatal_overdoses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...

    @property
    def pharmaceuticals(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing pharmaceutical cost information."
    @pharmaceuticals.setter
    def pharmaceuticals(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...

    @property
    def treatments(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing treatment cost information."
    @treatments.setter
    def treatments(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...


class CreationStatus:
    """
    Class enumerating possible creation statuses of the logger.

    Members:
      kError (-1)
      kSuccess (0)
      kExists (1)
      kNotCreated (2)
    """
    __members__: typing.ClassVar[dict[str, CreationStatus]
                                 # value = {'kError': <CreationStatus.kError: -1>, 'kSuccess': <CreationStatus.kSuccess: 0>, 'kExists': <CreationStatus.kExists: 1>, 'kNotCreated': <CreationStatus.kNotCreated: 2>}
                                 ]
    # value = <CreationStatus.kError: -1>
    kError: typing.ClassVar[CreationStatus]
    # value = <CreationStatus.kExists: 1>
    kExists: typing.ClassVar[CreationStatus]
    # value = <CreationStatus.kNotCreated: 2>
    kNotCreated: typing.ClassVar[CreationStatus]
    # value = <CreationStatus.kSuccess: 0>
    kSuccess: typing.ClassVar[CreationStatus]

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
    """
    Class grouping together matrices containing run history.

    Members:
      state
      overdoses
      intervention_admissions
    """

    def __init__(self) -> None:
        ...

    @property
    def intervention_admissions(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing intervention admission history."
    @intervention_admissions.setter
    def intervention_admissions(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...

    @property
    def overdoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing overdose history."
    @overdoses.setter
    def overdoses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...

    @property
    def state(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "The matrix containing state history"
    @state.setter
    def state(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...


class LogType:
    """
    Class enumerating logging levels.

    Members:
      kInfo (0)
      kWarn (1)
      kError (2)
      kDebug (3)
    """
    __members__: typing.ClassVar[dict[str, LogType]
                                 # value = {'kInfo': <LogType.kInfo: 0>, 'kWarn': <LogType.kWarn: 1>, 'kError': <LogType.kError: 2>, 'kDebug': <LogType.kDebug: 3>}
                                 ]
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
    """
    Class describing the RESPOND model simulation.
    """

    def __init__(self, log_name: str = 'console') -> None:
        ...

    def add_transition(self, transition: tuple[..., -1, 1, 0, -1, ..., collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]]) -> None:
        """
        Append a transition to the sequence of transitions.

        Args:
          transition: A tuple whose first element is a transition operation and second transition matrices.
        """

    def get_run_results(self) -> dict[int, HistoryStamp]:
        "Get the History from the simulation."

    def get_state(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "Getter for the state vector."

    def get_transitions(self) -> list[tuple[..., -1, 1, 0, -1, ..., list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]]]:
        "Getter for the transition operations."

    def run(self, num_steps: typing.SupportsInt) -> None:
        """
        Core function to Run the Markov model.

        Args:
          num_steps: The number of steps to run through the model.
        """

    def set_state(self, state_vector: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        """
        Setter for the state vector.

        Args:
          state_vector: The matrix describing the model state.
        """

    def set_transitions(self, transitions: collections.abc.Sequence[tuple[..., -1, 1, 0, -1, ..., collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]]]) -> None:
        """
        Setter for vector of transitions.

        Args:
          transitions: A sequence of tuples whose first elements are transition operations and second elements are transition matrices.
        """


class ResultSets:
    """
    Class grouping together final results.

    Members:
      summed_costs
      summed_life_years
      summed_utility
    """

    def __init__(self) -> None:
        ...

    @property
    def summed_costs(self) -> list[float]:
        "A list of summed costs."
    @summed_costs.setter
    def summed_costs(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...

    @property
    def summed_life_years(self) -> float:
        "Summed life years."
    @summed_life_years.setter
    def summed_life_years(self, arg0: typing.SupportsFloat) -> None:
        ...

    @property
    def summed_utility(self) -> float:
        "Summed utility."
    @summed_utility.setter
    def summed_utility(self, arg0: typing.SupportsFloat) -> None:
        ...


class Totals:
    """
    Class grouping together matrices containing total cost effectiveness information.

    Members:
      base
      discounted
    """
    base: ResultSets
    discounted: ResultSets

    def __init__(self) -> None:
        ...


class UtilityType:
    """
    Class enumerating ways which utility can be calculated.

    Members:
      kMin (0)
      kMult (1)
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


def behavior(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Behavior Transition.

    Args:
      state: The state vector
      transition: A sequence of length 1 containing the transition matrix for behavior changes.
    """


def calculate_life_years(history: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], discount: bool, discount_rate: typing.SupportsFloat) -> float:
    """
    Calculate the life years.
    """


def calculate_perspectives(history_over_time: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], perspectives: collections.abc.Sequence[str], healthcare_costs: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], aod_costs: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], fod_costs: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], pharma_costs: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], treatment_costs: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], discount: bool, discount_rate: typing.SupportsFloat) -> dict[str, dict[int, CostStamp]]:
    """
    Calculate the Cost Stamps for the given perspectives.
    """


def calculate_total_costs(costs: collections.abc.Mapping[typing.SupportsInt, CostStamp]) -> list[float]:
    """
    Calculate the total costs.
    """


def create_file_logger(logger_name: str, filepath: str) -> CreationStatus:
    """
    Creates a File Logger for use with RESPOND.
    """


def discount(data: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], discount_rate: typing.SupportsFloat, week: typing.SupportsInt, is_discrete: bool) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Calculates the Discount for the provided Vector given the discount rate, week, and flag to indicate if it is discrete or not.
    """


def discount_cost_stamp(cost_stamp: CostStamp, discount_rate: typing.SupportsFloat, week: typing.SupportsInt, is_discrete: bool) -> None:
    """
    Apply a discount to the given cost stamp.
    """


def intervention(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Intervention Transition.

    Args:
      transition: Sequence of length 2. Contains transition matrix for intervention changes and then the behavior changes once going through an intervention change.
    """


def log_debug(logger_name: str, message: str) -> None:
    """
    Logs a debug message to the log.
    """


def log_error(logger_name: str, message: str) -> None:
    """
    Logs an error message to the log.
    """


def log_info(logger_name: str, message: str) -> None:
    """
    Logs an info message to the log.
    """


def log_warning(logger_name: str, message: str) -> None:
    """
    Logs a warning message to the log.
    """


def migration(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Migrating Cohort.
    """


def mortality(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Mortality Transition.
    """


def overdose(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], transition: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Applies the Overdose Transition.
    """


def stamp_costs(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], healthcare_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], aod_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], fod_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], pharma_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], treatment_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> CostStamp:
    """
    Build a Cost Stamp.
    """


def stamp_costs_over_time(history_over_time: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], healthcare_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], aod_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], fod_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], pharma_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], treatment_costs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], discount: bool, discount_rate: typing.SupportsFloat) -> dict[int, CostStamp]:
    """
    Stamp costs over a history time period.
    """


def stamp_utilities(state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], utility: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
    """
    Build a Utility Stamp.
    """


def stamp_utilities_over_time(history: collections.abc.Mapping[typing.SupportsInt, HistoryStamp], utility: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], util_type: UtilityType, discount: bool, discount_rate: typing.SupportsFloat) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
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
