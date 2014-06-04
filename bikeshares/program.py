import pandas as pd

class TripSubset(pd.DataFrame):
    def by_station(self):
        started = self.groupby("start_station").size()
        ended = self.groupby("end_station").size()
        counts = pd.DataFrame({
            "trips_started": started,
            "trips_ended": ended,
            "trips_total": started + ended
        })
        return counts.reindex(counts.index.rename("station_id")).reset_index()

    def by_interval(self, interval, interval_name):
        counts = self.set_index("start_time")["bike_id"]\
            .resample(interval, how=len)
        return pd.DataFrame({
            "trips_total": counts
        }).reindex(counts.index.rename(interval_name))

    def by_day(self): return self.by_interval("D", "day")

    def by_month(self): return self.by_interval("MS", "month")

    def get_time_range(self, event="start"):
        times = self[event + "_time"]
        return (times.min(), times.max())
    
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
