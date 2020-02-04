from dateutil.rrule import rrule, MONTHLY
import datetime

import requests
import pandas
import numpy as np

class Weather(object):
    """
    Represent the weather station.
    """
    
    root_url = "http://www.astro.gla.ac.uk/observatory/weather/Observatory_weather/archive/"
    columns = ["Date", "Time", "Temp out", "High Temp", "Low Temp", "Out Humidity", "Dew point",
           "Wind speed", "Wind direction", "Wind run", "High speed", "High Direction", "Wind Chill",
           "Heat index", "THW Index", "Bar", "Rain", "Rain rate", "Heat D-D", "Cool D-D", 
           "In temp", "In Hum", "In dew", "In heat", "In EMC", "In Air density", "Wind samp", "Wind Tx", "ISS Recept", "Arc Int"
          ]
    def __init__(self):
        pass
    
    def _determine_files(self, start, end):
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
        end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
        files = [dt.strftime("%Y%m")+".txt" for dt in rrule(MONTHLY, dtstart=start, until=end)]
            
        return files
    
    def _download_files(self, start, end):
        files = self._determine_files(start, end)
        data = []
        for file in files:
            df = pandas.read_csv(f"{weather.root_url}/{file}", delimiter="\t", header=[0,1])
            df.columns = self.columns
            
            times = np.array([datetime.datetime.strptime(f"{x.Date} {x.Time}", "%d/%m/%y %H:%M") for i, x in df.iterrows()])
            df.index = times
            del(df['Date'])
            del(df['Time'])
            
            data.append(df)
        
        data = pandas.concat(data)

        return data


    
    def get_data(self, start, end):
        data = self._download_files(start, end)
        data = data.loc[slice(start, end)]
        
        return data
