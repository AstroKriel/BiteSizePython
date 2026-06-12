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
    std_value = float(numpy.std(values))
    if std_value == 0.0:
        raise ValueError("`values` has zero standard deviation; cannot normalise.")
    return float(numpy.mean(values)), std_value


##
## === NORMALISATION
##


def compute_standardised_values(
    values: NDArray,
    mean_value: float,
    std_value: float,
) -> NDArray:
    return (values - mean_value) / std_value


##
## === PROGRAM MAIN
##


def main() -> None:
    data = numpy.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    mean_value, std_value = compute_stats(data)
    standardised_values = compute_standardised_values(data, mean_value, std_value)
    print(standardised_values)


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
