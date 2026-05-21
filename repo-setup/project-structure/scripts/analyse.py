##
## === DEPENDENCIES
##

## stdlib
from pathlib import Path

## third-party
import matplotlib.pyplot as mpl_plot
import numpy

## local
from local_helpers.linear_fit import DataSeries, LineFit

##
## === CONSTANTS
##

TRUE_SLOPE = 2.5
TRUE_INTERCEPT = 1.3
NOISE_STD = 1.5
NUM_DATA_POINTS = 100
FIGURES_DIR = Path("figures")

##
## === PROGRAM MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
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
    fig_path = FIGURES_DIR / "output.png"
    fig.savefig(fig_path)
    print(f"\t> saved: {fig_path}")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
