## { MODULE

##
## === DEPENDENCIES
##

## third-party
import numpy

from numpy.typing import NDArray

##
## === NUMERIC HELPERS
##


def normalise(
    values: NDArray,
) -> NDArray:
    """
    Rescale `values` to the range [0, 1] using a min-max normalisation.

    The smallest element maps to 0.0 and the largest to 1.0. The output is
    always floating point, and keeps the same shape as the input.
    """
    values = values.astype(float)
    smallest = numpy.min(values)
    largest = numpy.max(values)
    return (values - smallest) / (largest - smallest)


def safe_log10(
    values: NDArray,
) -> NDArray:
    """
    Base-10 logarithm of `values`, returning `nan` wherever an element is not
    strictly positive (log10 is undefined for zero and negative inputs).
    """
    values = values.astype(float)
    result = numpy.full_like(values, numpy.nan)
    is_positive = values > 0.0
    result[is_positive] = numpy.log10(values[is_positive])
    return result


## } MODULE
