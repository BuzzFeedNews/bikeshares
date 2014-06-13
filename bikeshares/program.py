import pandas as pd

class TripSubset(object):
    aliased_methods = [
        "head", "tail",
        "groupby",
        "to_csv", "to_json", "to_dict", "get_values"
    ]

    def __init__(self, frame):
        self.df = pd.DataFrame(frame)
        for m in self.aliased_methods:
            setattr(self, m, getattr(self.df, m))

    def __getitem__(self, val):
        return self.df.__getitem__(val)

    def by_station(self):
        started = self.df.groupby("start_station").size()
        ended = self.df.groupby("end_station").size()
        counts = pd.DataFrame({
            "trips_started": started,
            "trips_ended": ended,
            "trips_total": started + ended
        })
        return counts.reindex(counts.index.rename("station_id")).reset_index()

    def by_interval(self, interval, interval_name):
        counts = self.df.set_index("start_time")["bike_id"]\
            .resample(interval, how=len)
        return pd.DataFrame({
            "trips_total": counts
        }).reindex(counts.index.rename(interval_name))

    def by_day(self): return self.df.by_interval("D", "day")

    def by_month(self): return self.df.by_interval("MS", "month")

    def get_time_range(self, event="start"):
        times = self.df[event + "_time"]
        return (times.min(), times.max())

    def from_time(self, time_ref, event="start"):
        selection = self.df.set_index(event + "_time").ix[time_ref:]
        return TripSubset(selection.reset_index())
    
    def to_time(self, time_ref, event="start"):
        selection = self.df.set_index(event + "_time").ix[:time_ref]
        return TripSubset(selection.reset_index())

    def between_times(self, t1, t2, event="start"):
        return self.from_time(t1, event).to_time(t2, event)

class BikeShareProgram(object):
    def __init__(self):
        self.trips = None
        self.stations = None

    def load_trips(self, *args, **kwargs):
        self.trips = TripSubset(self.parse_trips(*args, **kwargs))
        return self

    def load_stations(self, *args, **kwargs):
        self.stations = self.parse_stations(*args, **kwargs)
        return self
