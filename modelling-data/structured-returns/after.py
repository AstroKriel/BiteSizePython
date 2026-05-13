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

    @classmethod
    def from_field(
        cls,
        field: NDArray[Any],
    ) -> "FieldStats":
        return cls(
            min_value=float(field.min()),
            p16_value=float(numpy.percentile(field, q=16)),
            p50_value=float(numpy.percentile(field, q=50)),
            p84_value=float(numpy.percentile(field, q=84)),
            max_value=float(field.max()),
        )

    def __post_init__(
        self,
    ) -> None:
        if not (self.min_value <= self.p16_value <= self.p50_value <= self.p84_value <= self.max_value):
            raise ValueError(
                f"expected min <= p16 <= p50 <= p84 <= max; "
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
## === MAIN
##


def main() -> None:
    rng = numpy.random.default_rng(seed=0)
    rho = rng.uniform(
        low=0.1,
        high=10.0,
        size=(64, 64, 64),
    )
    stats = FieldStats.from_field(rho)
    ## everything is self-contained
    stats.print_summary()
    ## fields are named and unambiguous
    print(f"\t> {stats.p16_value}, {stats.p84_value}")


if __name__ == "__main__":
    main()
