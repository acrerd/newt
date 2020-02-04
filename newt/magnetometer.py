import requests
import datetime
import pandas
import numpy as np

from instruments import Instrument
from . import config

class Magnetometer(Instrument):
    """
    Represent the magnetometer.
    """
    
    root_url = config.get("magnetometer", "url")
    
    def __init__(self):
        pass
    
    def _determine_files(self, start, end):
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
        end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
        
        delta = end - start       # as timedelta
        files = []
        for i in range(delta.days + 1):
            day = start + datetime.timedelta(days=i)
            files.append("{}".format(day.strftime("%Y-%m-%d")))
            
        return files
    
    def _download_files(self, start, end):
        files = self._determine_files(start, end)
        data = []
        for file in files:
            download = requests.get("{}/{}.txt".format(self.root_url, file))
            
            download = np.fromstring(download.text, sep='\t').reshape(-1, 5)
            
            download = np.array(download, dtype=object)
            
            #download = self._apply_reductions(download)
            
            times = np.array([datetime.datetime.strptime(file, "%Y-%m-%d") + datetime.timedelta(seconds=x/1000) for x in download[:,0]])
            
            download[:,0] = times
            
            data.append(download)
        
        data = np.vstack(data)

        return data
    
    def _apply_reductions(self, data):
        #data[["x", "y", "z"]] += np.median(data[["x", "y", "z"]], axis=0)
        ftot = np.sum( data[["x", "y", "z"]], axis=0)
        #da = (data.index[-1] - data.index[0]).days
        ampcal = 1.1234615277 # 49891 / (ftot)
        
        data[["x", "y", "z"]] * (ampcal)
        return data
    
    def _apply_rotation(self, data):
        B_c = [16636.48633, -7215.19984936, 46478.2547421] # the field in the current axes (from a median of a lot of data)
        u_c = B_c/np.linalg.norm(B_c)

        B_t = [17264, -812, 46802] # the field in the target axes (from the reference website)
        u_t = B_t/np.linalg.norm(B_t)


        cross = np.cross(u_c, u_t)
        u = -cross/np.linalg.norm(cross)
        theta = np.arccos(np.dot(u_c, u_t))
        x = u[0]
        y = u[1]
        z = u[2]
        c = np.cos(theta)
        s = np.sin(theta)
        # rotation matrix by theta around u
        R = np.array([  [  c+x*x*(1-c), x*y*(1-c)-z*s,  x*z*(1-c)+y*s], 
                        [y*x*(1-c)+z*s,   c+y*y*(1-c),  y*z*(1-c)-x*s], 
                        [z*x*(1-c)-y*s, z*y*(1-c)+x*s,    c+z*z*(1-c)]  ])

        data[["x", "y", "z"]] = np.matmul(np.array(data[["x", "y", "z"]]).T, R)
        
        return data

    
    def get_data(self, start, end):
        data = self._download_files(start, end)
        dataframe = pandas.DataFrame(data[:,1:5], columns=("y", "x", "z", "temperature"), index=data[:,0])
        
        dataframe['H'] = (dataframe.x**2 + dataframe.y**2)**0.5
        dataframe['D'] = np.rad2deg(np.arctan2(np.array(dataframe.y.values, dtype=np.float64), np.array(dataframe.x.values, dtype=np.float64)))
        
        dataframe = dataframe.loc[slice(start, end)]
        dataframe = self._apply_reductions(dataframe)
        
        return dataframe
