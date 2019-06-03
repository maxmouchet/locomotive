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

    def find(self, str):
        res = self.df[self.df.sncf_id == str]
        if len(res) > 0:
            return res.iloc[0]
        else:
            return None
