##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass
from typing import Optional

## third-party
import matplotlib.pyplot as mpl_plot
import numpy

from numpy.typing import NDArray
from scipy.optimize import curve_fit as scipy_curve_fit

##
## === CONSTANTS
##

TRUE_SLOPE = 2.5
TRUE_INTERCEPT = 1.3
NOISE_STD = 1.5
NUM_DATA_POINTS = 100

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
        if self.y_sigmas is not None and (len(self.y_sigmas) != len(self.x_values)):
            raise ValueError(
                f"y_sigmas must have the same length as x_values; "
                f"got {len(self.y_sigmas)} and {len(self.x_values)}.",
            )


##
## === FIT RESULT
##


@dataclass(frozen=True)
class LineFit:
    data_series: DataSeries
    slope: float
    intercept: float
    slope_sigma: float
    intercept_sigma: float
    rms_residual: float

    @classmethod
    def from_fit(
        cls,
        data_series: DataSeries,
    ) -> "LineFit":
        popt, pcov = scipy_curve_fit(
            f=_linear_model,
            xdata=data_series.x_values,
            ydata=data_series.y_values,
            sigma=data_series.y_sigmas,
        )
        sigmas = numpy.sqrt(numpy.diag(pcov))
        y_fit = popt[0] * data_series.x_values + popt[1]
        rms_residual = float(numpy.sqrt(numpy.mean((data_series.y_values - y_fit)**2)))
        return cls(
            data_series=data_series,
            slope=popt[0],
            intercept=popt[1],
            slope_sigma=sigmas[0],
            intercept_sigma=sigmas[1],
            rms_residual=rms_residual,
        )

    def evaluate_at(
        self,
        x_values: NDArray,
    ) -> NDArray:
        return self.slope * x_values + self.intercept

    def compute_residuals(
        self,
    ) -> NDArray:
        return self.data_series.y_values - self.evaluate_at(self.data_series.x_values)

    def print_summary(
        self,
    ) -> None:
        print(f"\t> estimated slope: {self.slope:.4f} +/- {self.slope_sigma:.4f}")
        print(f"\t> estimated intercept: {self.intercept:.4f} +/- {self.intercept_sigma:.4f}")
        print(f"\t> rms residual: {self.rms_residual:.4f}")


##
## === PROGRAM MAIN
##


def main() -> None:
    x_values = numpy.linspace(
        start=0.0,
        stop=10.0,
        num=NUM_DATA_POINTS,
    )
    rng = numpy.random.default_rng(seed=0)
    random_values = rng.normal(
        loc=0.0,
        scale=NOISE_STD,
        size=x_values.size,
    )
    y_values = TRUE_SLOPE * x_values + TRUE_INTERCEPT + random_values
    data_series = DataSeries(
        x_values=x_values,
        y_values=y_values,
    )
    result = LineFit.from_fit(data_series=data_series)
    print(f"\t> true slope: {TRUE_SLOPE:.4f}")
    print(f"\t> true intercept: {TRUE_INTERCEPT:.4f}")
    result.print_summary()
    y_fit = result.evaluate_at(x_values=result.data_series.x_values)
    fig, ax = mpl_plot.subplots()
    ax.plot(
        result.data_series.x_values,
        result.data_series.y_values,
        linestyle="none",
        marker="o",
        markersize=4,
        color="blue",
        label="data points",
    )
    ax.plot(
        result.data_series.x_values,
        y_fit,
        linestyle="-",
        color="red",
        label=rf"fit: $y = {result.slope:.2f}\,x + {result.intercept:.2f}$",
    )
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend()
    fig.tight_layout()
    fig_name = "output.png"
    fig.savefig(fig_name)
    print(f"\t> saved: {fig_name}")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
