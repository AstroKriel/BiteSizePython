##
## === DEPENDENCIES
##

from dataclasses import dataclass

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


def _linear_model(
    x_values: NDArray,
    slope: float,
    intercept: float,
) -> NDArray:
    return slope * x_values + intercept


##
## === FIT RESULT
##


@dataclass(frozen=True)
class LineFit:
    slope: float
    intercept: float
    slope_sigma: float
    intercept_sigma: float

    @classmethod
    def from_fit(
        cls,
        x_values: NDArray,
        y_values: NDArray,
    ) -> "LineFit":
        popt, pcov = curve_fit(
            f=_linear_model,
            xdata=x_values,
            ydata=y_values,
        )
        sigmas = numpy.sqrt(numpy.diag(pcov))
        ## think about index order once, here, then never again
        return cls(
            slope=popt[0],
            intercept=popt[1],
            slope_sigma=sigmas[0],
            intercept_sigma=sigmas[1],
        )

    def __post_init__(
        self,
    ) -> None:
        if self.slope_sigma <= 0.0 or self.intercept_sigma <= 0.0:
            raise ValueError(
                f"expected positive sigmas; "
                f"got slope_sigma={self.slope_sigma:.4f}, intercept_sigma={self.intercept_sigma:.4f}.",
            )

    def evaluate_at(
        self,
        x_values: NDArray,
    ) -> NDArray:
        return self.slope * x_values + self.intercept

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
        return float(numpy.sqrt(numpy.mean(self.compute_residuals(x_ref, y_ref) ** 2)))


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

    result = LineFit.from_fit(x_values=x_values, y_values=y_values)
    result.print_summary()
    print(f"\t> rms residual: {result.rms_residual(x_values, y_values):.4f}")
    print(f"\t> first fitted value: {result.evaluate_at(x_values)[0]:.4f}")


if __name__ == "__main__":
    main()
