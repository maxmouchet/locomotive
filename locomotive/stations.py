import os

import geopy.distance as gp
import pandas as pd


class Stations:
    def __init__(self, fp=None):
        if fp is None:
            fp = os.path.join(os.path.dirname(__file__), "stations-lite.csv")
        self.df = pd.read_csv(fp, sep=";")

    @classmethod
    def coords(cls, station):
        return (station["latitude"], station["longitude"])

    @classmethod
    def distance(cls, s1, s2):
        return gp.distance(cls.coords(s1), cls.coords(s2)).km

    def find(self, q):
        # Try to find matching IDs
        # TODO: Optimize...
        if q in self.df.sncf_id.values:
            return self.df[self.df.sncf_id == q].iloc[0]
        # Try to find matching name
        # TODO: Partial search and rank results...
        if q in self.df.name.values:
            return self.df[self.df.name == q].iloc[0]
        return None
