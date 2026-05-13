# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "scipy",
# ]
# ///

##
## === DEPENDENCIES
##

import matplotlib.pyplot as plt
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
        scale=1.5,
        size=x_values.size,
    )

    popt, _ = curve_fit(
        f=linear_model,
        xdata=x_values,
        ydata=y_values,
    )
    slope = popt[0]
    intercept = popt[1]
    y_fit = linear_model(
        x_values=x_values,
        slope=slope,
        intercept=intercept,
    )

    print(f"\t> slope: {slope:.4f}")
    print(f"\t> intercept: {intercept:.4f}")

    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values, label="data", alpha=0.6)
    ax.plot(x_values, y_fit, label="fit", color="tab:red")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    fig.savefig("output.png", dpi=150)
    print(f"\t> saved: output.png")


if __name__ == "__main__":
    main()
