##
## === DEPENDENCIES
##

import numpy
from numpy.typing import NDArray
from scipy.optimize import curve_fit

##
## === CONSTANTS
##

TRUE_SLOPE = 2.5
TRUE_INTERCEPT = 1.3
NOISE_STD = 0.5

##
## === FIT FUNCTION
##


def linear_model(
    x_values: NDArray,
    slope: float,
    intercept: float,
) -> NDArray:
    return slope * x_values + intercept


##
## === MAIN
##


def main() -> None:
    rng = numpy.random.default_rng(seed=0)
    x_values = numpy.linspace(start=0.0, stop=10.0, num=50)
    y_values = TRUE_SLOPE * x_values + TRUE_INTERCEPT + rng.normal(
        loc=0.0,
        scale=NOISE_STD,
        size=x_values.size,
    )

    popt, pcov = curve_fit(
        f=linear_model,
        xdata=x_values,
        ydata=y_values,
    )
    sigmas = numpy.sqrt(numpy.diag(pcov))

    ## popt[0]? popt[1]? you have to check the model signature every time
    print(f"\t> slope: {popt[0]:.4f} +/- {sigmas[0]:.4f}")
    print(f"\t> intercept: {popt[1]:.4f} +/- {sigmas[1]:.4f}")

    ## passing raw arrays around: every callsite carries the same index knowledge
    y_fit = popt[0] * x_values + popt[1]
    rms = float(numpy.sqrt(numpy.mean((y_values - y_fit) ** 2)))
    print(f"\t> rms residual: {rms:.4f}")


if __name__ == "__main__":
    main()
