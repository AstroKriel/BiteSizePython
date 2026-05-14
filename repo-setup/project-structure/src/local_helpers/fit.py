##
## === DEPENDENCIES
##

## standard library
from dataclasses import dataclass

## third-party
import numpy
from numpy.typing import NDArray
from scipy.optimize import curve_fit

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
        return cls(
            slope=popt[0],
            intercept=popt[1],
            slope_sigma=sigmas[0],
            intercept_sigma=sigmas[1],
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
