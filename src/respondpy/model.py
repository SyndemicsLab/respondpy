from __future__ import annotations

from ._core.model import (
    Respond,
    calculate_discount,
    calculate_costs,
    calculate_utilities,
    calculate_life_years,
    calculate_total_costs
)

__all__ = (
    "Respond",
    "calculate_discount",
    "calculate_costs",
    "calculate_utilities",
    "calculate_life_years",
    "calculate_total_costs"
)


def __dir__() -> list[str]:
    return list(__all__)
