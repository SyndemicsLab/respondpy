################################################################################
# File: markov.pyi                                                             #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-02                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import typing
import collections.abc

import numpy as np

from .types import HistoryStamp
from .transition import Transition


class Markov:
    """
    Class describing the RESPOND model simulation.
    """

    def __init__(self, log_name: str = 'console') -> None:
        ...

    def add_transition(self, tr: Transition) -> None:
        """
        Append a transition to the sequence of transitions.

        Args:
          transition: A tuple whose first element is a transition operation and second transition matrices.
        """

    def get_run_results(self) -> dict[int, HistoryStamp]:
        "Get the History from the simulation."

    def get_state(self) -> typing.Annotated[np.typing.NDArray[np.float64], "[m, 1]"]:
        "Getter for the state vector."

    def get_transitions(self) -> collections.abc.Sequence[Transition]:
        "Getter for the transition operations."

    def run(self, num_steps: typing.SupportsInt) -> None:
        """
        Core function to Run the Markov model.

        Args:
          num_steps: The number of steps to run through the model.
        """

    def set_state(self, state_vector: typing.Annotated[np.typing.ArrayLike, np.float64, "[m, 1]"]) -> None:
        """
        Setter for the state vector.

        Args:
          state_vector: The matrix describing the model state.
        """

    def set_transitions(self, transitions: collections.abc.Sequence[Transition]) -> None:
        """
        Setter for vector of transitions.

        Args:
          transitions: A sequence of tuples whose first elements are transition operations and second elements are transition matrices.
        """
