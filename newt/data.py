"""
The functions and classes for finding and interacting 
with observatory data are located in this file.
"""

import pandas
from astropy.time import Time
import numpy, os
from dateutil.relativedelta import relativedelta

class Channel(object):
    """
    A channel is designed to hold the data from a single instrument, 
    stored at a specific data rate. Examples might be the temperature 
    sensor on the weather station, or the total power output of a radio 
    telescope.
    """

    def __init__(self, instrument, sample_rate, directory):
        """
        Initialise the channel.

        Parameters
        ----------
        instrument : str
           The instrument which will be queried for data.
        sample_rate : int
           The sample rate at which data is stored in this channel.
        directory : str
           The directory in which the data is stored.
        """

        self.instrument = instrument
        self.directory = directory


    def fetch(self, start, end):
        """
        Fetch data from this channel between the start and end times specified.
        
        Parameters
        ----------
        start, end : str
           The start and end times.

        Returns
        -------
        data : numpy array-like
        """

        start = Time(start, scale='utc')
        end = Time(end, scale='utc')
        
        # Get the list of data files first
        files = []
        date = start.datetime
        while date <= end.datetime:
            files.append( os.path.join(self.directory, "{:%Y%m}.txt".format(date)))
            date += relativedelta(months=1)

        output = []
        # Open the data files, and add any data to the output array
        # which is inside the requested timespan.
        for filename in files:
            data = pandas.read_csv(filename, delimiter="\t", parse_dates=[[0,1]], header=[0,1], index_col=0, dayfirst=True)
            output.append(data.ix[start.datetime:end.datetime])

        return output
