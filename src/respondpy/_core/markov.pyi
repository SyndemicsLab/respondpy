################################################################################
# File: markov.pyi                                                             #
# Project: respondpy                                                           #
# Created Date: 2026-01-08                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-08                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

import typing
import collections.abc

import numpy
import numpy.typing

from .types import HistoryStamp, vector_1d, vector_of_matrices, transition_function, transition


class Markov:
    """
    Class describing the RESPOND model simulation.
    """

    def __init__(self, log_name: str = 'console') -> None:
        ...

    def add_transition(self, transition: transition) -> None:
        """
        Append a transition to the sequence of transitions.

        Args:
          transition: A tuple whose first element is a transition operation and second transition matrices.
        """

    def get_run_results(self) -> dict[int, HistoryStamp]:
        "Get the History from the simulation."

    def get_state(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        "Getter for the state vector."

    def get_transitions(self) -> list[transition]:
        "Getter for the transition operations."

    def run(self, num_steps: typing.SupportsInt) -> None:
        """
        Core function to Run the Markov model.

        Args:
          num_steps: The number of steps to run through the model.
        """

    def set_state(self, state_vector: vector_1d) -> None:
        """
        Setter for the state vector.

        Args:
          state_vector: The matrix describing the model state.
        """

    def set_transitions(self, transitions: collections.abc.Sequence[transition]) -> None:
        """
        Setter for vector of transitions.

        Args:
          transitions: A sequence of tuples whose first elements are transition operations and second elements are transition matrices.
        """
