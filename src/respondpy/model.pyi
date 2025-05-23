"""
A submodule containing the model components for RESPOND.
"""
from __future__ import annotations
import numpy
import respondpy.data_ops
__all__ = ['Respond', 'calculate_costs', 'calculate_discount', 'calculate_life_years', 'calculate_total_costs', 'calculate_utilities']
class Respond:
    def __init__(self, log_name: str = 'console') -> None:
        ...
    def get_history(self) -> respondpy.data_ops.History:
        ...
    def run(self, arg0: respondpy.data_ops.DataLoader) -> None:
        ...
def calculate_costs(arg0: respondpy.data_ops.History, arg1: respondpy.data_ops.CostLoader, arg2: list[str], arg3: bool, arg4: float) -> list[respondpy.data_ops.Cost]:
    """
    Calculates the Costs of the provided History.
    """
def calculate_discount(arg0: numpy.ndarray[numpy.float64[..., ..., ...]], arg1: float, arg2: int, arg3: bool) -> numpy.ndarray[numpy.float64[..., ..., ...]]:
    """
    Calculates the Discount for the provided Matrix3d.
    """
def calculate_life_years(arg0: respondpy.data_ops.History, arg1: bool, arg2: float) -> float:
    """
    Calculate the Life Years of the provided History.
    """
def calculate_total_costs(arg0: list[respondpy.data_ops.Cost]) -> list[float]:
    """
    Calculate the Total Costs of the provided History.
    """
def calculate_utilities(arg0: respondpy.data_ops.History, arg1: respondpy.data_ops.UtilityLoader, arg2: respondpy.data_ops.UtilityType, arg3: bool, arg4: float) -> dict[int, numpy.ndarray[numpy.float64[..., ..., ...]]]:
    """
    Calculate the Utilities of the provided History.
    """
