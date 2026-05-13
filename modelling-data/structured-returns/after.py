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
                f"got {self.min_value}, {self.p16_value}, {self.p50_value}, {self.p84_value}, {self.max_value}.",
            )

    def print_summary(
        self,
    ) -> None:
        print(f"\t> min: {self.min_value:.3f}")
        print(f"\t> p16: {self.p16_value:.3f}")
        print(f"\t> p50: {self.p50_value:.3f}")
        print(f"\t> p84: {self.p84_value:.3f}")
        print(f"\t> max: {self.max_value:.3f}")


##
## === FUNCTIONS
##


def compute_field_stats(
    field: NDArray[Any],
) -> FieldStats:
    min_value = field.min()
    p16_value = numpy.percentile(field, 16)
    p50_value = numpy.percentile(field, 50)
    p84_value = numpy.percentile(field, 84)
    max_value = field.max()
    return FieldStats(
        min_value=min_value,
        p16_value=p16_value,
        p50_value=p50_value,
        p84_value=p84_value,
        max_value=max_value,
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
    print(f"\t> {stats.p16_value}, {stats.p84_value}")


if __name__ == "__main__":
    main()
