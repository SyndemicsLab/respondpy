################################################################################
# File: types.pyi                                                              #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-28                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import typing
import collections.abc

import numpy
import numpy.typing

# ensure these match the types defined in respondpy/__init__.py
# They are included there because we expose the types for usage in the library
# (this only works for type hinting, not usage)

vector_1d: typing.TypeAlias = typing.Annotated[numpy.typing.ArrayLike,
                                               numpy.float64, "[m, 1]"]

vector_of_matrices: typing.TypeAlias = collections.abc.Sequence[
    typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]

transition_function: typing.TypeAlias = typing.Callable[[vector_1d,
                                                         vector_of_matrices, HistoryStamp], vector_1d]

transition: typing.TypeAlias = tuple[transition_function, vector_of_matrices]


class HistoryStamp:
    """
    Class grouping together matrices containing run history.

    Members:
      state
      total_overdoses
      fatal_overdoses
      background_mortality
      intervention_admissions
    """

    def __init__(self) -> None:
        ...

    @property
    def intervention_admissions(self) -> vector_1d:
        "The matrix containing intervention admission history."
    @intervention_admissions.setter
    def intervention_admissions(self, arg0: vector_1d) -> None:
        ...

    @property
    def total_overdoses(self) -> vector_1d:
        "The matrix containing overdose history."
    @total_overdoses.setter
    def total_overdoses(self, arg0: vector_1d) -> None:
        ...

    @property
    def fatal_overdoses(self) -> vector_1d:
        "The matrix containing fatal overdose history."
    @fatal_overdoses.setter
    def fatal_overdoses(self, arg0: vector_1d) -> None:
        ...

    @property
    def background_mortality(self) -> vector_1d:
        "The matrix containing background_mortality history."
    @background_mortality.setter
    def background_mortality(self, arg0: vector_1d) -> None:
        ...

    @property
    def state(self) -> vector_1d:
        "The matrix containing state history"
    @state.setter
    def state(self, arg0: vector_1d) -> None:
        ...


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
    def fatal_overdoses(self) -> vector_1d:
        "The matrix containing fatal overdose cost information."
    @fatal_overdoses.setter
    def fatal_overdoses(self, arg0: vector_1d) -> None:
        ...

    @property
    def healthcare(self) -> vector_1d:
        "The matrix containing healthcare cost information."
    @healthcare.setter
    def healthcare(self, arg0: vector_1d) -> None:
        ...

    @property
    def non_fatal_overdoses(self) -> vector_1d:
        "The matrix containing non-fatal overdose cost information."
    @non_fatal_overdoses.setter
    def non_fatal_overdoses(self, arg0: vector_1d) -> None:
        ...

    @property
    def pharmaceuticals(self) -> vector_1d:
        "The matrix containing pharmaceutical cost information."
    @pharmaceuticals.setter
    def pharmaceuticals(self, arg0: vector_1d) -> None:
        ...

    @property
    def treatments(self) -> vector_1d:
        "The matrix containing treatment cost information."
    @treatments.setter
    def treatments(self, arg0: vector_1d) -> None:
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


kMin: UtilityType  # value = <UtilityType.kMin: 0>
kMult: UtilityType  # value = <UtilityType.kMult: 1>
