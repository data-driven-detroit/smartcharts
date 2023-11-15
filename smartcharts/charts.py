"""
charts.py has all the classes for the different types of charts and how they
are built within the tree.
"""

from typing import Protocol
from enum import Enum
from functools import reduce

from smartcharts.datapoint import DataPoint


class ColumnWidth(float, Enum):
    """
    This is how you set the column width on the DataDesign that you're building.
    It will help avoid over-filling the row, or giving the js incorrect column
    widths.
    """

    QUARTER = 1 / 4
    THIRD = 1 / 3
    HALF = 1 / 2
    TWO_THIRDS = 2 / 3
    THREE_QUARTERS = 3 / 4
    FULL = 1


    def hyphenated_name(self) -> str:
        return "column-" + self.name.replace("_", "-").lower()


class Chart(Protocol):
    title: str
    identifier: str
    _width: ColumnWidth

    def collect_shopping_list(self) -> set[str]:
        ...

    def populate(self, *args, **kwargs) -> dict[str, str | dict]:
        ...

    @property
    def width(self) -> str:
        """Returns the string value of the enum assigned to _width"""
        ...


class Factoid(Protocol):
    """
    These are little snippets of text with one or more embedded, calculated 
    values. How this works isn't quite figured out yet.
    """
    template: str

    def collect_shopping_list(self) -> set[str]:
        ...

    def render(self, *args, **kwargs) -> str:
        ...


class StatList:
    """
    On CR, this is a single value.
    """
    name: str
    identifier: str
    _width: ColumnWidth
    stat: DataPoint

    def collect_shopping_list(self) -> set[str]:
        return self.stat.collect_shopping_list()

    def populate(self, *args, **kwargs):
        return {
            "stat": self.stat.evaluate(*args, **kwargs),
        }


class ColumnChart:
    """
    A basic vertical bar chart.
    """
    name: str
    identifier: str
    _width: ColumnWidth
    columns: list[DataPoint]

    def collect_shopping_list(self) -> set[str]:
        return reduce(
            lambda a, b: a | b,
            (column.collect_shopping_list() for column in self.columns),
            set(),
        )

    def sub_populate(self, *args, **kwargs):
        """
        This function will populate the chart, but skip any of the
        metadata embellishments.
        """
        ...

    def populate(self, *args, **kwargs):
        return {
            "name": self.name,
            "chart_type": "column",
            **{
                column.name: column.evaluate(*args, **kwargs)
                for column in self.columns
            },
        }


class DoughnutChart:
    """
    A basic pie chart with a hole in the middle.
    """
    name: str
    identifier: str
    _width: ColumnWidth
    slices: list[DataPoint]

    def collect_shopping_list(self) -> set[str]:
        ...

    def populate(self, *args, **kwargs):
        return {
            "name": self.name,
            "chart_type": "pie",
            **{
                slice.name: slice.evaluate(*args, **kwargs)
                for slice in self.slices
            },
        }


class GroupedColumnChart:
    """
    A grouped version of column charts.
    """

    name: str
    identifier: str
    _width: ColumnWidth
    child_charts: list[ColumnChart]    

    def collect_shopping_list(self) -> set[str]:
        return reduce(
            lambda a, b: a | b,
            (chart.collect_shopping_list() for chart in self.child_charts),
            set(),
        )

    def populate(self, *args, **kwargs):
        return {
            "name": self.name,
            "chart_type": "grouped_column",
            **{
                chart.name: chart.sub_populate(*args, **kwargs)
                for chart in self.child_charts
            },
        }


class LineChart:
    name: str
    identifier: str
    _width: ColumnWidth
    points: list[DataPoint]    

    def collect_shopping_list(self) -> set[str]:
        return reduce(
            lambda a, b: a | b,
            (point.collect_shopping_list() for point in self.points),
            set(),
        )

    def populate(self, *args, **kwargs):
        return {
            "name": self.name,
            "chart_type": "line",
            **{
                point.name: point.evaluate(*args, **kwargs)
                for point in self.points
            },
        }
