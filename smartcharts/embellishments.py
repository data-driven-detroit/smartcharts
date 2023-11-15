"""
Embellishments are either tuples of object name, or functions provided to nodes in a profile tree that add
extra content to the output dictionary. They should take the same args & kwargs
as the rest of the datapoints.
"""

from typing import Callable, Any

Embellishment =  tuple[str, Any] | Callable[[Any], tuple[str, Any]]


def adorn(embellishment: Embellishment, *args, **kwargs):
    if callable(embellishment):
        return embellishment(*args, **kwargs)
    return embellishment


# an example embellishment

def example_embellishment(*args, **kwargs) -> tuple[str, dict[str, str | int]]:
    object = {
        "name": "Name of place for the data",
        "year": 2021
    }

    return "name", object
