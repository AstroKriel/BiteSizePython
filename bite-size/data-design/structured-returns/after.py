##
## === DEPENDENCIES
##

from dataclasses import dataclass
from typing import Any

import numpy
from numpy.typing import NDArray


##
## === FIELD STATS
##


@dataclass(frozen=True)
class FieldStats:
    min_value: float
    p16_value: float
    p50_value: float
    p84_value: float
    max_value: float

    def __post_init__(
        self,
    ) -> None:
        if not (self.min_value <= self.p16_value <= self.p50_value <= self.p84_value <= self.max_value):
            raise ValueError(
                f"expected min_value <= p16_value <= p50_value <= p84_value <= max_value; "
                f"got {self.min_value}, {self.p16_value}, {self.p50_value}, {self.p84_value}, {self.max_value}."
            )

    def print_summary(
        self,
    ) -> None:
        width = 6
        print(f"  min: {self.min_value:{width}.3f}")
        print(f"  p16: {self.p16_value:{width}.3f}")
        print(f"  p50: {self.p50_value:{width}.3f}")
        print(f"  p84: {self.p84_value:{width}.3f}")
        print(f"  max: {self.max_value:{width}.3f}")


##
## === FUNCTIONS
##


def compute_field_stats(
    field: NDArray[Any],
) -> FieldStats:
    return FieldStats(
        min_value=float(field.min()),
        p16_value=float(numpy.percentile(field, 16)),
        p50_value=float(numpy.percentile(field, 50)),
        p84_value=float(numpy.percentile(field, 84)),
        max_value=float(field.max()),
    )


##
## === MAIN
##


def main() -> None:
    rng = numpy.random.default_rng(seed=0)
    rho = rng.uniform(
        low=0.1,
        high=10.0,
        size=(64, 64, 64),
    )
    stats = compute_field_stats(rho)
    ## everything is self-contained
    stats.print_summary()
    ## fields are named and unambiguous
    print(stats.p16_value, stats.p84_value)


if __name__ == "__main__":
    main()
