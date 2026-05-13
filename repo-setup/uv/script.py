##
## === DEPENDENCIES
##

from dataclasses import dataclass

import matplotlib.pyplot as plt
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


##
## === MAIN
##


def main() -> None:
    rng = numpy.random.default_rng(seed=0)
    x_values = numpy.linspace(start=0.0, stop=10.0, num=50)
    y_values = 2.5 * x_values + 1.3 + rng.normal(
        loc=0.0,
        scale=1.5,
        size=x_values.size,
    )

    result = LineFit.from_fit(
        x_values=x_values,
        y_values=y_values,
    )
    result.print_summary()

    y_fit = result.evaluate_at(x_values=x_values)

    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values, label="data", alpha=0.6)
    ax.plot(x_values, y_fit, label="fit", color="tab:red")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    fig_name = "output.png"
    fig.savefig(fig_name, dpi=150)
    print(f"\t> saved: {fig_name}")


if __name__ == "__main__":
    main()
