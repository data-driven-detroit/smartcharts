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

## Embellishments

... more to come

## Some downsides

... more to come

## TODOs

- Add metadata handling
- Add more tests
- Copy over and test Django template rendering
- Bring over GeoBuilder class from SDC/HIP
