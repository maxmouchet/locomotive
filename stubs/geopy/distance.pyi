from typing import Tuple

class Distance:
    @property
    def km(self) -> float: ...

def distance(a: Tuple[float, float], b: Tuple[float, float]) -> Distance: ...
