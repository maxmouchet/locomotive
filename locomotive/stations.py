"""
Train stations.
"""

import os

import geopy.distance as gp
import pandas as pd
import difflib


class Stations:
    """
    A train stations database.
    See https://github.com/trainline-eu/stations.
    """

    def __init__(self, fp=None):
        if fp is None:
            fp = os.path.join(os.path.dirname(__file__), "data", "stations-lite.csv")
        self.df = pd.read_csv(fp, sep=";")

    @classmethod
    def coords(cls, station):
        """
        Get train station coordinates in geopy format.
        """
        return (station["latitude"], station["longitude"])

    @classmethod
    def distance(cls, s1, s2):
        """
        Get distance in kilometers between two train stations.
        """
        return gp.distance(cls.coords(s1), cls.coords(s2)).km

    def find(self, q):
        # Try to find matching IDs
        # TODO: Optimize...
        if q in self.df.sncf_id.values:
            return self.df[self.df.sncf_id == q].iloc[0]
        # Try to find matching name
        else:
            try:
                best_match = difflib.get_close_matches(q, self.df.name.values, n=1)[0]
                return self.df[self.df.name == best_match].iloc[0]
            except:
                pass
        return None
