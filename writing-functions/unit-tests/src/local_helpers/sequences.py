## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from typing import Any

##
## === SEQUENCE HELPERS
##


def chunk(
    items: list[Any],
    *,
    size: int,
) -> list[list[Any]]:
    """
    Split `items` into consecutive chunks of length `size`.

    The final chunk is shorter when `len(items)` is not an exact multiple of
    `size`. The original ordering is preserved.
    """
    return [
        items[start : start + size]
        for start in range(0, len(items), size)
    ]


def running_totals(
    values: list[float],
) -> list[float]:
    """
    Return the cumulative sums of `values`: element `i` of the result is the
    sum of `values[0 .. i]`. An empty input gives an empty list.
    """
    totals: list[float] = []
    running = 0.0
    for value in values:
        running += value
        totals.append(running)
    return totals


## } MODULE
