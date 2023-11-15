"""
The datapoint module shows how the basic numeric values work
with datadesign, and how to write the main protocol for the system,
the 'DataPoint.'
"""

from typing import Protocol
from dataclasses import dataclass


class Value(Protocol):
    value: int | float
    error: int | float


@dataclass
class Numeric(frozen=True, slots=True):
    value: int | float
    error: int | float


@dataclass
class Percent(frozen=True, slots=True):
    numerator: Numeric
    denominator: Numeric

    @property
    def value(self):
        return NotImplementedError("Implement value calculation for percent.")

    @property
    def error(self):
        raise NotImplementedError("Implement error calculation for percent.")  



class DataPoint(Protocol):
    name: str

    def collect_shopping_list(self) -> set[str]:
        """
        OPTIONAL: Used if you need to query the stucture ahead of time
        to determine what data that you need if you have to make an api call
        to get it.
        """
        ...

    def evaluate(self) -> dict[str, Value]:
        """
        This function isn't required if the data doesn't need to be called
        beforehand, it's used if you need to query the stucture ahead of time
        to determine what data that you need if you have to make an api call
        to get it.
        """
        ...
