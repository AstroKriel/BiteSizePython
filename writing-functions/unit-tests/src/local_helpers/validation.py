## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from typing import Any

##
## === INPUT GUARDS
##


def require_positive(
    value: float,
    *,
    name: str = "value",
) -> float:
    """
    Return `value` unchanged if it is strictly positive, otherwise raise
    `ValueError`. Use at the top of a function to reject bad inputs early.
    """
    if value <= 0.0:
        raise ValueError(
            f"{name} must be positive, got {value}.",
        )
    return value


def require_non_empty(
    items: list[Any],
    *,
    name: str = "items",
) -> list[Any]:
    """
    Return `items` unchanged if it contains at least one element, otherwise
    raise `ValueError`.
    """
    if len(items) == 0:
        raise ValueError(
            f"{name} must not be empty.",
        )
    return items


## } MODULE
