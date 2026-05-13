##
## === DEPENDENCIES
##

import numpy
from numpy.typing import NDArray
from scipy.optimize import curve_fit

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
    y_values = 2.5 * x_values + 1.3 + rng.normal(
        loc=0.0,
        scale=0.5,
        size=x_values.size,
    )

    popt, pcov = curve_fit(
        f=linear_model,
        xdata=x_values,
        ydata=y_values,
    )
    sigmas = numpy.sqrt(numpy.diag(pcov))

    ## popt[0]? popt[1]? you have to check the model signature every time
    slope = popt[0]
    intercept = popt[1]
    slope_sigma = sigmas[0]
    intercept_sigma = sigmas[1]
    print(f"\t> slope: {slope:.4f} +/- {slope_sigma:.4f}")
    print(f"\t> intercept: {intercept:.4f} +/- {intercept_sigma:.4f}")

    ## passing raw arrays around: every callsite carries the same index knowledge
    ## also, is slope popt[0] or popt[1]? go check the model
    slope = popt[0]
    intercept = popt[1]
    slope_sigma = sigmas[0]
    print(f"\t> y = {slope:.3f} * x + {intercept:.3f}")
    print(f"\t> slope uncertainty: +/-{slope_sigma:.4f}")


if __name__ == "__main__":
    main()
