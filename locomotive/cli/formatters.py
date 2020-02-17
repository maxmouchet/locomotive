import datetime as dt
import json
from pathlib import Path
from typing import Any, Callable, Iterable, Union

import attr
import babel.dates
from jinja2 import Environment, FileSystemLoader
from money.money import Money

from ..models import Journey


class JSONFormatter:
    """
    JSON output.
    """

    @staticmethod
    def serialize(obj: Any) -> Union[dict, str]:
        if hasattr(obj, "__attrs_attrs__"):
            return attr.asdict(obj)
        if isinstance(obj, dt.datetime):
            return obj.isoformat()
        if isinstance(obj, Money):
            return {"amount": float(obj.amount), "currency": obj.currency.name}
        raise TypeError

    def print(self, journeys: Iterable[Journey], fn: Callable = print) -> None:
        fn(json.dumps(list(journeys), default=self.serialize, indent=4))


class PrettyFormatter:
    """
    Human-readable pretty-printed output.
    """

    @staticmethod
    def format_datetime(x: dt.datetime) -> str:
        return str(babel.dates.format_datetime(x, "dd/MM/YYYY HH'h'mm"))

    @staticmethod
    def format_time(x: dt.datetime) -> str:
        return str(babel.dates.format_time(x, "HH'h'mm"))

    @staticmethod
    def format_timedelta(x: dt.timedelta) -> str:
        delta = x.seconds
        hours, remainder = divmod(delta, 3600)
        minutes, _ = divmod(remainder, 60)
        return "{:02}h{:02}m".format(int(hours), int(minutes))

    def print(self, journeys: Iterable[Journey], fn: Callable = print) -> None:
        templates = Path(__file__).parent.joinpath("templates")
        env = Environment(
            loader=FileSystemLoader(str(templates)),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["format_time"] = self.format_time
        env.filters["format_timedelta"] = self.format_timedelta
        env.filters["format_datetime"] = self.format_datetime

        for journey in journeys:
            template = env.get_template("journey.txt")
            out = template.render(journey=journey)
            out = out.replace("<b>", "\033[1m")
            out = out.replace("</b>", "\033[0m")
            fn(out)
