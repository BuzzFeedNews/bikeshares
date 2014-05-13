import bikeshares
import pandas as pd
import numpy as np

def convert_rider_gender(x):
    if x == 0: return np.nan
    if x == 1: return "M"
    if x == 2: return "F"
    raise Exception("Unrecognized gender variable: {0}".format(x))

def convert_rider_type(x):
    if x == "Subscriber": return "member"
    if x == "Customer": return "non-member"
    raise Exception("Unrecognized rider type: {0}".format(x))

class CitiBike(bikeshares.program.BikeShareProgram):
    def parse_trips(self, data_path):
        parsed = pd.read_csv(data_path,
            usecols=["starttime", "stoptime", "tripduration",
                "start station id", "end station id",
                "bikeid", "usertype", "gender", "birth year" ],
            parse_dates=["starttime", "stoptime"]) 
        
        mapped = pd.DataFrame({
            "start_time": parsed["starttime"],
            "start_station": parsed["start station id"],
            "end_time": parsed["stoptime"],
            "end_station": parsed["end station id"],
            "duration": parsed["tripduration"],
            "bike_id": parsed["bikeid"],
            "rider_type": parsed["usertype"].apply(convert_rider_type),
            "rider_gender": parsed["gender"].apply(convert_rider_gender),
            "rider_birthyear": parsed["birth year"]
        })

        return mapped

    def parse_stations(self, data_path):
        parsed = pd.read_csv(data_path,
            usecols=[ "start station id", "start station name",
                "start station latitude", "start station longitude" ])

        mapped = pd.DataFrame({
            "id": parsed["start station id"],
            "name": parsed["start station name"],
            "lat": parsed["start station latitude"],
            "lng": parsed["start station longitude"]
        }).groupby("id").first().reset_index()

        return mapped

