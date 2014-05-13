import bikeshares
import pandas as pd
import numpy as np

def convert_rider_gender(x):
    if type(x) != str and np.isnan(x): return np.nan
    if x == "Male": return "M"
    if x == "Female": return "F"
    raise Exception("Unrecognized gender variable: {0}".format(x))

def convert_rider_type(x):
    if x == "Subscriber": return "member"
    if x == "Customer": return "non-member"
    raise Exception("Unrecognized rider type: {0}".format(x))

class Divvy(bikeshares.program.BikeShareProgram):
    def parse_trips(self, data_path):
        parsed = pd.read_csv(data_path,
            dtype=dict(gender="O"),
            usecols=[ "starttime", "stoptime", "tripduration",
                "from_station_id", "to_station_id",
                "bikeid", "usertype", "gender", "birthday" ],
            parse_dates=["starttime", "stoptime"]) 
        
        mapped = pd.DataFrame({
            "start_time": parsed["starttime"],
            "start_station": parsed["from_station_id"],
            "end_time": parsed["stoptime"],
            "end_station": parsed["to_station_id"],
            "duration": parsed["tripduration"],
            "bike_id": parsed["bikeid"],
            "rider_type": parsed["usertype"].apply(convert_rider_type),
            "rider_gender": parsed["gender"].apply(convert_rider_gender),
            "rider_birthyear": parsed["birthday"]
        })

        return mapped

    def parse_stations(self, data_path):
        parsed = pd.read_csv(data_path,
            usecols=[ "id", "name", "dpcapacity",
                "online date", "latitude", "longitude" ],
            parse_dates=["online date"])

        mapped = pd.DataFrame({
            "id": parsed["id"],
            "name": parsed["name"],
            "lat": parsed["latitude"],
            "lng": parsed["longitude"],
            "capacity": parsed["dpcapacity"],
            "install_date": parsed["online date"]
        }).groupby("id").first().reset_index()

        return mapped

