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
    if not isinstance(values, numpy.ndarray):
        raise TypeError("`values` must be an NDArray.")
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
    if not isinstance(values, numpy.ndarray):
        raise TypeError("`values` must be an NDArray.")
    if not isinstance(mean_value, (float, numpy.floating)):
        raise TypeError("`mean_value` must be a float.")
    if not isinstance(std_value, (float, numpy.floating)):
        raise TypeError("`std_value` must be a float.")
    if std_value == 0.0:
        raise ValueError("`std_value` must not be zero.")
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
