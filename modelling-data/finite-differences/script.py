##
## === DEPENDENCIES
##

## stdlib
from pathlib import Path

## third-party
import matplotlib.pyplot as plt
import numpy
from numpy.typing import NDArray

##
## === CONSTANTS
##

X_MIN = 0.0
X_MAX = 2.0 * numpy.pi
NUM_POINTS_LIST = [10, 20, 50, 100, 200, 500]
FIGURES_DIR = Path("figures")

##
## === FUNCTIONS
##


def f(
    x: NDArray,
) -> NDArray:
    return numpy.sin(2.0 * x) + numpy.cos(x)


def df_exact(
    x: NDArray,
) -> NDArray:
    return 2.0 * numpy.cos(2.0 * x) - numpy.sin(x)


##
## === MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    dx_values = []
    errors = []
    for num_points in NUM_POINTS_LIST:
        x = numpy.linspace(
            start=X_MIN,
            stop=X_MAX,
            num=num_points,
            endpoint=False,
        )
        dx = float(x[1] - x[0])
        y = f(x)
        df_numerical = numpy.gradient(y, dx)
        rms_error = float(numpy.sqrt(numpy.mean((df_numerical - df_exact(x))**2)))
        dx_values.append(dx)
        errors.append(rms_error)
        print(f"\t> n={num_points:4d}, dx={dx:.4f}, rms error={rms_error:.2e}")
    dx_arr = numpy.array(dx_values)
    errors_arr = numpy.array(errors)
    ref = errors_arr[0] * (dx_arr / dx_arr[0])**2
    fig, ax = plt.subplots()
    ax.loglog(dx_arr, errors_arr, "o-", label="RMS error")
    ax.loglog(
        dx_arr,
        ref,
        "--",
        color="gray",
        label=r"$O(\Delta x^2)$ reference",
    )
    ax.set_xlabel(r"grid spacing $\Delta x$")
    ax.set_ylabel("RMS error")
    ax.legend()
    fig_path = FIGURES_DIR / "convergence.png"
    fig.savefig(fig_path, dpi=150)
    print(f"\t> saved: {fig_path}")


if __name__ == "__main__":
    main()
