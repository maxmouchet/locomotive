from collections import defaultdict
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from money.money import Money

from .models import Journey, Segment


class JourneyDiffType(Enum):
    NoChange = auto()
    # New price < Old price
    LowerPrice = auto()
    # New price > Old price
    HigherPrice = auto()
    # Journey is now full
    Unavailable = auto()
    # Journey is not full anymore
    Available = auto()
    # Journey doesn't exists anymore
    Removed = auto()
    # Journey has been added
    Added = auto()


# Enjoy this beauty :-)
class JourneyDiff:
    old: Optional[Journey]
    new: Optional[Journey]
    diff_type: Optional[JourneyDiffType]

    def __init__(self, old: Optional[Journey], new: Optional[Journey]):
        self.old = old
        self.new = new

        if old and not new:
            self.diff_type = JourneyDiffType.Removed
        elif new and not old:
            self.diff_type = JourneyDiffType.Added
        elif old and new:
            if old.lowest_price and not new.lowest_price:
                self.diff_type = JourneyDiffType.Unavailable
            elif new.lowest_price and not old.lowest_price:
                self.diff_type = JourneyDiffType.Available
            # Explicit old *and* new branch for mypy
            elif old.lowest_price and new.lowest_price:
                if new.lowest_price < old.lowest_price:
                    self.diff_type = JourneyDiffType.LowerPrice
                elif new.lowest_price > old.lowest_price:
                    self.diff_type = JourneyDiffType.HigherPrice
                else:
                    self.diff_type = JourneyDiffType.NoChange
            else:
                self.diff_type = JourneyDiffType.NoChange
        else:
            self.diff_type = None

    @property
    def price_diff(self) -> Optional[Money]:
        if self.old and self.new and self.old.lowest_price and self.new.lowest_price:
            return self.new.lowest_price - self.old.lowest_price
        return None


def journeys_diff(
    old_journeys: List[Journey], new_journeys: List[Journey]
) -> List[JourneyDiff]:
    # We don't use sets here since we don't want to consider the same journey
    # with different prices, as different journeys.
    # We consider that two journeys are the same, if all their segments are identical.
    journeys: Dict[Tuple[Segment, ...], Dict[str, Journey]] = defaultdict(dict)

    for journey in old_journeys:
        journeys[journey.segments]["old"] = journey

    for journey in new_journeys:
        journeys[journey.segments]["new"] = journey

    diffs = []
    for v in journeys.values():
        diff = JourneyDiff(v.get("old"), v.get("new"))
        diffs.append(diff)

    return diffs
