import bikeshares
import pandas as pd
import numpy as np

def convert_rider_gender(x):
    if type(x) != str and np.isnan(x): return np.nan
    if x == "Male": return "M"
    if x == "Female": return "F"
    raise Exception("Unrecognized gender variable: {0}".format(x))

def convert_rider_type(x):
    if x == "Registered": return "member"
    if x == "Casual": return "non-member"
    raise Exception("Unrecognized rider type: {0}".format(x))

class Hubway(bikeshares.program.BikeShareProgram):
    def parse_trips(self, data_path):
        parsed = pd.read_csv(data_path,
            dtype=dict(zip_code="O"),
            na_values=["NA"],
            usecols=[ "start_date", "end_date", "duration",
                "start_station", "end_station", "bike_nr",
                "subscription_type", "zip_code", "birth_date", "gender" ],
            parse_dates=["start_date", "end_date"]) 
        
        mapped = pd.DataFrame({
            "start_time": parsed["start_date"],
            "start_station": parsed["start_station"],
            "end_time": parsed["end_date"],
            "end_station": parsed["end_station"],
            "duration": parsed["duration"],
            "bike_id": parsed["bike_nr"],
            "rider_type": parsed["subscription_type"].apply(convert_rider_type),
            "rider_gender": parsed["gender"].apply(convert_rider_gender),
            "rider_birthyear": parsed["birth_date"]
        })

        return mapped

    def parse_stations(self, data_path):
        parsed = pd.read_csv(data_path,
            usecols=[ "id", "station",
                "install_date", "last_day", "nb_docks",
                "lat", "lng" ],
            parse_dates=["install_date", "last_day"])

        mapped = pd.DataFrame({
            "id": parsed["id"],
            "name": parsed["station"],
            "lat": parsed["lat"],
            "lng": parsed["lng"],
            "capacity": parsed["nb_docks"],
            "install_date": parsed["install_date"],
            "removal_date": parsed["last_day"]
        }).groupby("id").first().reset_index()

        return mapped

