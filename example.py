from dataclasses import dataclass
from collections import namedtuple

from smartcharts.datapoint import DataPoint, Value
from smartcharts.charts import StatList, ColumnChart, ColumnWidth
from smartcharts.profile_node import Row


class District:
    """
    A mock for a django db table. Only has 'all', 'filter' and 'first'
    """

    class Objects:
        def __init__(self, table):
            self.table = table

        def all(self):
            return type(self)([self.table])

        def filter(self, **kwargs):
            return type(self)([
                row
                for row in self.table
                if all(getattr(row, kwarg) == val for kwarg, val in kwargs.items())
            ])

        def first(self):
            try:
                return self.table[0]
            except IndexError:
                return None

        
    Row = namedtuple("Row", "district population")

    objects = Objects([
        Row("district_1", 14001),
        Row("district_2", 15000),
        Row("district_3", 16000),
        Row("district_4", 17000),
        Row("district_5", 18000),
        Row("district_6", 19000),
        Row("district_7", 11000),
        Row("district_8", 11100),
    ])


@dataclass
class ParcelDataPoint:
    name: str
    column: str

    def collect_shopping_list(self, *args, **kwargs):
        pass

    def evaluate(self, council_district: str) -> dict[str, int | float]:
        return {
            "this": getattr(
                District.objects.filter(district=council_district).first(), self.column
            )
        }


row = Row(
    name="General indicators",
    children=[
        StatList(
            name="Population of District",
            _width=ColumnWidth.QUARTER,
            identifier="some_name",
            stat=ParcelDataPoint("population", "population"),
        ),
    ],
)


def django_view(district_name):
    context = row.populate(district_name)

    return context


if __name__ == "__main__":
    print(django_view("district_1"))
    print(django_view("district_3"))
