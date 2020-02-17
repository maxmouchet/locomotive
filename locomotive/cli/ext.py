import datetime as dt
from typing import Iterator

import click
import dateparser as dp


class DateParseParamType(click.ParamType):
    name = "DATE"

    def convert(self, value, param, ctx):  # type: ignore
        settings = {"TIMEZONE": "Europe/Paris", "RETURN_AS_TIMEZONE_AWARE": True}
        return dp.parse(value, settings=settings)


def daterange(
    start: dt.datetime, stop: dt.datetime, step: dt.timedelta
) -> Iterator[dt.datetime]:
    curr = start
    while curr < stop:
        yield curr
        curr += step
