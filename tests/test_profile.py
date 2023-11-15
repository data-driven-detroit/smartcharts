# All the user needs to do is write a class following the DataPoint
# protocol
from dataclasses import dataclass
import logging
import pytest

from smartcharts.datapoint import Numeric
from smartcharts.profile_node import Row, Section, Profile
from smartcharts.charts import StatList, ColumnWidth

logger = logging.getLogger()


@pytest.fixture
def NoArgDataPoint():
    class CustomDataPoint:
        def collect_shopping_list(self) -> set[str]:
            raise NotImplementedError("This isn't required for our use case.")

        def evaluate(self) -> dict[str, Numeric]:
            return {"this": Numeric(6, 2)}

    return CustomDataPoint


@pytest.fixture
def simple_db():
    class Database:
        def __init__(self, table: dict[str, Numeric]):
            self.table = table

        def execute(self, query: str):
            return self.table.get(query)

    return Database(
        {
            "alpha": Numeric(1000, 10),
            "beta": Numeric(5000, 20),
            "gamma": Numeric(500, 23),
            "ziti": Numeric(450, 2),
        }
    )


@pytest.fixture
def complex_db():
    class Database:
        def __init__(self, tables: dict[str, dict[str, Numeric]]):
            self.tables = tables

        def execute(self, query: str):
            column, table = query.split(" in ")
            try:
                return self.tables.get(table)[column]
            except (KeyError, AttributeError) as e:
                match e:
                    case AttributeError():
                        raise LookupError(f"The relation {table} is not in the database.")
                    case KeyError():
                        raise LookupError(f"The column {column} is not available on relation {table}.")

    return Database(
        {
            "alpha": {
                "rho": Numeric(1000, 10),
                "pi": Numeric(9999, 12),
                "xerox": Numeric(7777, 2),
            },
            "beta":{
                "rho": Numeric(1030, 10),
                "pi": Numeric(1090, 12),
                "xerox": Numeric(7010, 4),
            },
            "gamma": {
                "rho": Numeric(1088, 22),
                "pi": Numeric(1000, 0),
                "xerox": Numeric(101, 1),
            },
            "ziti": {
                "rho": Numeric(10, 0),
                "pi": Numeric(99999, 2),
                "xerox": Numeric(1239, 343),
            },
        }
    )


@pytest.fixture
def NeedsArgDataPoint(simple_db):
    class DataPoint:
        def collect_shopping_list(self) -> set[str]:
            raise NotImplementedError("This isn't required for our use case.")

        def evaluate(self, letter: str) -> dict[str, Numeric]:
            query = letter
            return simple_db.execute(query)

    return DataPoint


@pytest.fixture
def AlmostRealDataPoint(complex_db):
    @dataclass
    class DataPoint:
        table: str

        def collect_shopping_list(self) -> set[str]:
            raise NotImplementedError("This isn't required for our use case.")

        def evaluate(self, letter: str) -> dict[str, Numeric]:
            query = f"{letter} in {self.table}"
            return complex_db.execute(query)

    return DataPoint


def test_implement_datapoint():
    class CustomDataPoint:
        def collect_shopping_list(self) -> set[str]:
            raise NotImplementedError("This isn't required for our use case.")

        def evaluate(self) -> dict[str, Numeric]:
            return {"this": Numeric(6, 2)}

    result = CustomDataPoint()

    assert result.evaluate()["this"] == Numeric(6, 2)


def test_populate_row(NoArgDataPoint):
    row = Row(
        name="some_row",
        children=[
            StatList(
                name="First Stat",
                identifier="first_stat",
                _width=ColumnWidth.QUARTER,
                stat=NoArgDataPoint(),
            ),
            StatList(
                name="Second Stat",
                identifier="second_stat",
                _width=ColumnWidth.QUARTER,
                stat=NoArgDataPoint(),
            ),
        ],
    )

    assert row.populate() # Basically asserting now that this doesn't break, will need more detail later


def test_datapoint_with_populate_args(NeedsArgDataPoint):
    datapoint = NeedsArgDataPoint()
    assert datapoint.evaluate("gamma") == Numeric(500, 23)


def test_datapoint_with_init_and_populate_args(AlmostRealDataPoint):
    datapoint = AlmostRealDataPoint("ziti")

    assert datapoint.evaluate("xerox") == Numeric(1239, 343)
    assert datapoint.evaluate("pi") == Numeric(99999, 2)


def test_populate_row_with_populate_args(NeedsArgDataPoint):
    assert False


def test_populate_row_with_init_and_populate_args(AlmostRealDataPoint):
    assert False

