from typing import Union
from dataclasses import dataclass, field
from functools import reduce

from smartcharts.embellishments import Embellishment, adorn
from smartcharts.charts import Chart


@dataclass
class ProfileNode:
    name: str
    children: list[Union["ProfileNode", Chart]]
    embellishments: list[Embellishment] = field(default_factory=list)

    def collect_shopping_list(self):
        return reduce(
            lambda a, b: a | b,
            (child.collect_shopping_list() for child in self.children),
            set(),
        )

    def populate(self, *args, **kwargs):
        return {
            "name": self.name,
            "children": {
                child.name: child.populate(*args, **kwargs)
                for child in self.children
            },
            **dict(
                adorn(embellishment, *args, *kwargs)
                for embellishment in self.embellishments
            ),
        }


# Setting up aliases right now, but this might change in the future.


class Row(ProfileNode):
    children: list[Chart]

    def __post_init__(self):
        total_width = sum(child._width.value for child in self.children)

        if total_width <= 1.01:
            raise ValueError(
                f"The row {self.name}, is too wide. Make sure the chart widths sum to less than one."
            )


class Section(ProfileNode):
    pass


class Profile(ProfileNode):
    pass
