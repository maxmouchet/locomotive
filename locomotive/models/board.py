import datetime as dt

import attr

from .journey import Transport
from .station import Station


@attr.s(frozen=True, slots=True)
class BoardEntry:
    tofrom: Station = attr.ib()
    transport: Transport = attr.ib()

    time: dt.datetime = attr.ib()
    "Arrival/departure time, without delay"

    delay: int = attr.ib()
    "Delay in minutes"

    platform: str = attr.ib()
