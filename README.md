# bikeshares

Bicycle-sharing services publish [trip-history data](https://github.com/BuzzFeedNews/bikeshare-data-sources) in a variety of layouts and represent common variables, such as the rider's gender, in disparate ways. `bikeshares`, a Python library, standardizes this data. Currently supporting:

- New York City — Citi Bike
- Chicago — Divvy
- Boston — Hubway

## Installation

`pip install bikeshares`

## Usage

`bikeshares` assumes you have already [downloaded trip history and/or station data](https://github.com/BuzzFeedNews/bikeshare-data-sources) from the bikeshare services themselves. The `bikeshares` parsers read these files, and convert their data into a standardized set of fields. See [*Fields*](#fields) for details. Example usage:

```python
from bikeshares.programs.chicago import Divvy
divvy = Divvy()

divvy.load_trips("path/to/trips.csv")
divvy.load_stations("path/to/stations.csv")

trips_per_station = divvy.trips.by_station()
```

### Methods/Properties

Each supported bikeshare service has its own Python class. Each of those classes has two main methods:

- `load_trips("path/to/file.csv")`
- `load_stations("path/to/file.csv")`

Both methods expect the [main CSV files published](https://github.com/BuzzFeedNews/bikeshare-data-sources) by the bikeshare services themselves as their first (and, typically, only) argument. Each program also has two main properties:

- `trips`, a light wrapper around a [pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/dsintro.html) of each loaded trip. `trips.df` provides direct access to the DataFrame. `trips` itself has several handy methods:
	- `trips.by_station()`, which returns trip counts per station
	- `trips.by_day()`, which returns daily trip counts
	- `trips.by_month()`, which returns monthly trip counts
	- `trips.get_time_range()`, which returns the start times of the earliest and latest loaded trips.
	- `trips.from_time(time)`, `trips.to_time(time)`, and `trips.between_times(time_1, time_2)`, which let you return time-bounded subsets of the loaded trips.

- `stations`, a [pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/dsintro.html) containing each station.

### Fields

__Trips__ contain the following fields:

- `start_time`
- `start_station` (station ID)
- `end_time`
- `end_station` (station ID)
- `duration` (in seconds)
- `bike_id`
- `rider_type` ("member" or "non-member")
- `rider_gender` ("M", "F", or null; for members only, where available)
- `rider_birthyear` (four-digit year; for members only, where available)

__Stations__ contain the following fields:

- `id`
- `name`
- `lat`
- `lng`
- `capacity`
- `install_date`
- `removal_date`

## Bikeshare Services Currently Supported 

- `bikeshares.programs.nyc.CitiBike`
	- Note: Citi Bike does not currently publish a CSV of stations. Instead, `CitiBike.load_stations()` pulls station information from Citi Bike's trip-history CSVs.

- `bikeshares.programs.chicago.Divvy`
- `bikeshares.programs.boston.Hubway`
