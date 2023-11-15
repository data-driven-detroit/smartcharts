from dataclasses import dataclass
from functools import reduce

from smartcharts.embellishments import Embellishment, adorn


@dataclass
class ProfileNode:
    title: str
    children: list["ProfileNode"]
    embellishments: list[Embellishment]

    def collect_shopping_list(self):
        return reduce(
            lambda a, b: a | b,
            (child.collect_shopping_list() for child in self.children),
            set(),
        )

    def populate(self, *args, **kwargs):
        return {
            "children": {
                child.title: child.populate(*args, **kwargs)
                for child in self.children
            },
            **dict(adorn(embellishment, *args, *kwargs) for embellishment in self.embellishments)
        }
