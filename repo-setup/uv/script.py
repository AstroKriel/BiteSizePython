##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass

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
        popt, pcov = scipy_curve_fit(
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
        print(f"\t> estimated slope: {self.slope:.4f} +/- {self.slope_sigma:.4f}")
        print(f"\t> estimated intercept: {self.intercept:.4f} +/- {self.intercept_sigma:.4f}")


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
    result = LineFit.from_fit(
        x_values=x_values,
        y_values=y_values,
    )
    print(f"\t> true slope: {TRUE_SLOPE:.4f}")
    print(f"\t> true intercept: {TRUE_INTERCEPT:.4f}")
    result.print_summary()
    y_fit = result.evaluate_at(x_values=x_values)
    fig, ax = mpl_plot.subplots()
    ax.plot(
        x_values,
        y_values,
        linestyle="none",
        marker="o",
        markersize=4,
        color="blue",
        label="data points",
    )
    ax.plot(
        x_values,
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
