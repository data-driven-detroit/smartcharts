# Smart Charts

A library to easily structure data profiles to work with the Census Reporter charts.js.


## Installing from github

```console
pip install git+https://github.com/data-driven-detroit/smartcharts
```


## Basic usage

The first step to use the profile maker is to write your own DataPoint class that fulfill the following protocol:

```python
class DataPoint(Protocol):
    name: str

    def collect_shopping_list(self) -> set[str]:
        """
        OPTIONAL: Used if you need to query the stucture ahead of time
        to determine what data that you need if you have to make an api call
        to get it.
        """
        ...

    def evaluate(self, *args, **kwargs) -> dict[str, Value]:
        """
        This function that takes args and kwargs and builds the data point.
        These could be simple as a string to look up in a database, or a full
        dictionary loaded with API data.
        """
        ...
```

Once you've built the custom profile you can then build out an entire profile with that DataPoint.


```python

@dataclass
class DistrictDataPoint:
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

@dataclass
class CensusDataPoint:
    name: str
    acs_var_name: str

    def collect_shopping_list(self, *args, **kwargs):
        return {self.acs_var_name}

    def evaluate(self, api_response: dict[str, float], council_district: str) -> dict[str, int | float]:
        # This does some complicated reading of the census api_response to aggregate 
        # tracts to the council district.


row = Row(
    name="General indicators",
    children=[
        StatList(
            name="Population of District",
            _width=ColumnWidth.QUARTER,
            identifier="some_name",
            stat=ParcelDataPoint("Total population", "population"),
        ),
    ],
)


def mock_django_view(district_name):
    context = row.populate(district_name)

    return context

print(mock_django_view("district_1"))

```

This will return a dictionary that looks like this:


```python
{
    "name": "General indicators", # Name of the row
    "children": {
        "Population of District": {"stat": {"this": 16000}} # StatList rendered
    },
}
```


## Embellishments

... more to come

## Some downsides

... more to come

## TODOs

- Add metadata handling
- Add more tests
- Test Django template rendering
- Bring over GeoBuilder class from SDC/HIP
