from __future__ import annotations
import numpy
import numpy.typing
import typing
__all__: list[str] = ['History']
class History:
    __hash__: typing.ClassVar[None] = None
    def __copy__(self) -> History:
        ...
    def __eq__(self, arg0: History) -> bool:
        """
        Check equality of History objects (name, log_name, and state).
        """
    def __init__(self, name: str = 'state', log_name: str = 'console') -> None:
        ...
    def __ne__(self, arg0: History) -> bool:
        """
        Check inequality of History objects.
        """
    def add_state(self, state: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], timestep: typing.SupportsInt = -1) -> None:
        """
        Add a state vector at a given timestep (-1 for auto-increment).
        """
    def clear(self) -> None:
        """
        Clear all stored state history.
        """
    def get_history_name(self) -> str:
        """
        Get the name of the history object.
        """
    def get_log_name(self) -> str:
        """
        Get the log name used for logging.
        """
    def get_state_as_vector(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]:
        """
        Get the state as a vector, padding missing timesteps with zero vectors.
        """
    def get_state_map(self) -> dict[int, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]:
        """
        Get the state map (timestep -> state vector).
        """
