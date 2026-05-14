##
## === DEPENDENCIES
##

## standard library
from pathlib import Path

## third-party
import matplotlib.pyplot as plt
import numpy

## local
from local_helpers.fit import LineFit

##
## === CONSTANTS
##

TRUE_SLOPE = 2.5
TRUE_INTERCEPT = 1.3
NOISE_STD = 1.5
FIGURES_DIR = Path("figures")

##
## === MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    rng = numpy.random.default_rng(seed=0)
    x_values = numpy.linspace(start=0.0, stop=10.0, num=50)
    y_values = TRUE_SLOPE * x_values + TRUE_INTERCEPT + rng.normal(
        loc=0.0,
        scale=NOISE_STD,
        size=x_values.size,
    )

    result = LineFit.from_fit(x_values=x_values, y_values=y_values)
    result.print_summary()

    y_fit = result.evaluate_at(x_values=x_values)

    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values, color="blue", label="data points", alpha=0.6)
    ax.plot(x_values, y_fit, label="fit", color="red")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    fig_path = FIGURES_DIR / "output.png"
    fig.savefig(fig_path, dpi=150)
    print(f"\t> saved: {fig_path}")


if __name__ == "__main__":
    main()
