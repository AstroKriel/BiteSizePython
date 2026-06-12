##
## === DEPENDENCIES
##

## third-party
import numpy

from numpy.typing import NDArray

##
## === STATISTICS
##


def compute_stats(
    values: NDArray,
) -> tuple[float, float]:
    if values.size == 0:
        raise ValueError("`values` must not be empty.")
    std = float(numpy.std(values))
    if std == 0.0:
        raise ValueError("`values` has zero standard deviation; cannot normalise.")
    return float(numpy.mean(values)), std


##
## === NORMALISATION
##


def normalise(
    values: NDArray,
    mean: float,
    std: float,
) -> NDArray:
    return (values - mean) / std


##
## === PROGRAM MAIN
##


def main() -> None:
    data = numpy.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    mean, std = compute_stats(data)
    normalised = normalise(data, mean, std)
    print(normalised)


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
