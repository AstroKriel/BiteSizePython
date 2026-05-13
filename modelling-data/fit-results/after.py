##
## === DEPENDENCIES
##

from dataclasses import dataclass

import numpy
from numpy.typing import NDArray
from scipy.optimize import curve_fit

##
## === FIT RESULT
##


@dataclass(frozen=True)
class LineFit:
    slope: float
    intercept: float
    slope_sigma: float
    intercept_sigma: float

    def evaluate_at(
        self,
        domain: NDArray,
    ) -> NDArray:
        return self.slope * domain + self.intercept

    def print_summary(
        self,
    ) -> None:
        print(f"\t> slope: {self.slope:.4f} +/- {self.slope_sigma:.4f}")
        print(f"\t> intercept: {self.intercept:.4f} +/- {self.intercept_sigma:.4f}")

    def compute_residuals(
        self,
        x_ref: NDArray,
        y_ref: NDArray,
    ) -> NDArray:
        return y_ref - self.evaluate_at(x_ref)

    def rms_residual(
        self,
        x_ref: NDArray,
        y_ref: NDArray,
    ) -> float:
        return float(
            numpy.sqrt(
                numpy.mean(self.compute_residuals(x_ref, y_ref)**2),
            ),
        )


##
## === FIT FUNCTION
##


def linear_model(
    x_values: NDArray,
    slope: float,
    intercept: float,
) -> NDArray:
    return slope * x_values + intercept


def fit_line(
    x_values: NDArray,
    y_values: NDArray,
) -> LineFit:
    popt, pcov = curve_fit(
        f=linear_model,
        xdata=x_values,
        ydata=y_values,
    )
    sigmas = numpy.sqrt(numpy.diag(pcov))
    ## think about index order once, here, then never again
    return LineFit(
        slope=popt[0],
        intercept=popt[1],
        slope_sigma=sigmas[0],
        intercept_sigma=sigmas[1],
    )


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

    result = fit_line(x_values, y_values)
    result.print_summary()

    y_fit = result.evaluate_at(x_values)
    first_fitted_value = y_fit[0]
    print(f"\t> first fitted value: {first_fitted_value:.4f}")

    rms_residual = result.rms_residual(x_values, y_values)
    print(f"\t> rms residual: {rms_residual:.4f}")


if __name__ == "__main__":
    main()
