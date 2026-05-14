##
## === DEPENDENCIES
##

from dataclasses import dataclass
from typing import Optional

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
## === DATA SERIES
##


@dataclass(frozen=True)
class DataSeries:
    x_values: NDArray
    y_values: NDArray
    y_sigmas: Optional[NDArray] = None

    def __post_init__(
        self,
    ) -> None:
        if len(self.x_values) != len(self.y_values):
            raise ValueError(
                f"x_values and y_values must have the same length; "
                f"got {len(self.x_values)} and {len(self.y_values)}.",
            )
        if self.y_sigmas is not None and len(self.y_sigmas) != len(self.x_values):
            raise ValueError(
                f"y_sigmas must have the same length as x_values; "
                f"got {len(self.y_sigmas)} and {len(self.x_values)}.",
            )


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
        data_series: DataSeries,
    ) -> "LineFit":
        popt, pcov = curve_fit(
            f=_linear_model,
            xdata=data_series.x_values,
            ydata=data_series.y_values,
            sigma=data_series.y_sigmas,
        )
        sigmas = numpy.sqrt(numpy.diag(pcov))
        ## think about index order once, here, then never again
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

    def compute_residuals(
        self,
        data_series: DataSeries,
    ) -> NDArray:
        return data_series.y_values - self.evaluate_at(data_series.x_values)

    def rms_residual(
        self,
        data_series: DataSeries,
    ) -> float:
        return float(numpy.sqrt(numpy.mean(self.compute_residuals(data_series=data_series) ** 2)))


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

    data_series = DataSeries(x_values=x_values, y_values=y_values)
    result = LineFit.from_fit(data_series=data_series)
    result.print_summary()
    print(f"\t> rms residual: {result.rms_residual(data_series=data_series):.4f}")
    print(f"\t> first fitted value: {result.evaluate_at(x_values=x_values)[0]:.4f}")


if __name__ == "__main__":
    main()
