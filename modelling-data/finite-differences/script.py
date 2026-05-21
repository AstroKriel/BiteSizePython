##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

## third-party
import matplotlib.pyplot as mpl_plot
import numpy

from numpy.typing import NDArray

##
## === CONSTANTS
##

X_MIN = 0.0
X_MAX = 2.0 * numpy.pi
NUM_POINTS_LIST = [10, 20, 50, 100, 200, 500]
NUM_POINTS_EXAMPLE = 20
NUM_POINTS_EXACT = 300
FIGURES_DIR = Path("figures")

##
## === FUNCTIONS
##


def f(x: NDArray) -> NDArray:
    return numpy.sin(2.0 * x) + numpy.cos(x)


def df_exact(x: NDArray) -> NDArray:
    return 2.0 * numpy.cos(2.0 * x) - numpy.sin(x)


##
## === STENCILS
##


def forward_difference(y: NDArray, h: float) -> NDArray:
    return (y[1:] - y[:-1]) / h


def centered_2nd(y: NDArray, h: float) -> NDArray:
    return (y[2:] - y[:-2]) / (2.0 * h)


def centered_4th(y: NDArray, h: float) -> NDArray:
    return (-y[4:] + 8.0 * y[3:-1] - 8.0 * y[1:-3] + y[:-4]) / (12.0 * h)


def centered_6th(y: NDArray, h: float) -> NDArray:
    return (y[6:] - 9.0 * y[5:-1] + 45.0 * y[4:-2] - 45.0 * y[2:-4] + 9.0 * y[1:-5] - y[:-6]) / (60.0 * h)


##
## === METHOD
##


@dataclass(frozen=True)
class Method:
    name: str
    fn: Callable[[NDArray, float], NDArray]
    order: int
    x_slice: slice
    color: str


METHODS = [
    Method(name="forward O(h)",    fn=forward_difference, order=1, x_slice=slice(None, -1), color="tab:blue"),
    Method(name="centered O(h^2)", fn=centered_2nd,       order=2, x_slice=slice(1, -1),   color="tab:orange"),
    Method(name="centered O(h^4)", fn=centered_4th,       order=4, x_slice=slice(2, -2),   color="tab:green"),
    Method(name="centered O(h^6)", fn=centered_6th,       order=6, x_slice=slice(3, -3),   color="tab:red"),
]

##
## === COMPUTE
##


def compute_rms_error(method: Method, num_points: int) -> tuple[float, float]:
    x = numpy.linspace(X_MIN, X_MAX, num=num_points, endpoint=False)
    h = float(x[1] - x[0])
    y = f(x)
    df_num = method.fn(y, h)
    df_an = df_exact(x[method.x_slice])
    rms = float(numpy.sqrt(numpy.mean((df_num - df_an) ** 2)))
    return h, rms


##
## === PLOT
##


def plot_function(ax, x_exact: NDArray, y_exact: NDArray) -> None:
    ax.plot(x_exact, y_exact, color="black")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("function")


def plot_derivative_approx(
    ax,
    x_exact: NDArray,
    df_exact_values: NDArray,
    x_example: NDArray,
    y_example: NDArray,
    h_example: float,
) -> None:
    ax.plot(x_exact, df_exact_values, color="black", label="exact", zorder=5)
    for method in METHODS:
        df_num = method.fn(y_example, h_example)
        ax.plot(
            x_example[method.x_slice],
            df_num,
            "o",
            color=method.color,
            label=method.name,
            markersize=4,
        )
    ax.set_xlabel("x")
    ax.set_ylabel("df/dx")
    ax.set_title("derivative approximations")
    ax.legend(fontsize=8)


def plot_convergence(ax) -> None:
    for method in METHODS:
        h_values = []
        rms_values = []
        for num_points in NUM_POINTS_LIST:
            h, rms = compute_rms_error(method, num_points)
            h_values.append(h)
            rms_values.append(rms)
        h_arr = numpy.array(h_values)
        rms_arr = numpy.array(rms_values)
        ax.loglog(h_arr, rms_arr, "o-", color=method.color, label=method.name)
        h_ref = numpy.array([h_arr[0], h_arr[-1]])
        ref = rms_arr[0] * (h_ref / h_ref[0]) ** method.order
        ax.loglog(h_ref, ref, "--", color=method.color, alpha=0.4)
    ax.set_xlabel(r"$\Delta x$")
    ax.set_ylabel("RMS error")
    ax.set_title("convergence")
    ax.legend(fontsize=8)


def plot_residuals(ax, x_example: NDArray, y_example: NDArray, h_example: float) -> None:
    for method in METHODS:
        df_num = method.fn(y_example, h_example)
        df_an = df_exact(x_example[method.x_slice])
        residual = numpy.abs(df_num - df_an)
        ax.semilogy(
            x_example[method.x_slice],
            residual,
            "o-",
            color=method.color,
            label=method.name,
            markersize=4,
        )
    ax.set_xlabel("x")
    ax.set_ylabel("absolute error")
    ax.set_title("pointwise error")
    ax.legend(fontsize=8)


##
## === PROGRAM MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)

    x_exact = numpy.linspace(X_MIN, X_MAX, num=NUM_POINTS_EXACT)
    y_exact = f(x_exact)
    df_exact_values = df_exact(x_exact)

    x_example = numpy.linspace(X_MIN, X_MAX, num=NUM_POINTS_EXAMPLE, endpoint=False)
    h_example = float(x_example[1] - x_example[0])
    y_example = f(x_example)

    for method in METHODS:
        for num_points in NUM_POINTS_LIST:
            h, rms = compute_rms_error(method, num_points)
            print(f"\t> {method.name}: n={num_points}, dx={h:.4f}, rms={rms:.2e}")

    fig, axes = mpl_plot.subplots(2, 2, figsize=(10, 8))

    plot_function(axes[0, 0], x_exact, y_exact)
    plot_derivative_approx(axes[0, 1], x_exact, df_exact_values, x_example, y_example, h_example)
    plot_convergence(axes[1, 0])
    plot_residuals(axes[1, 1], x_example, y_example, h_example)

    fig.tight_layout()
    fig_path = FIGURES_DIR / "convergence.png"
    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    print(f"\t> saved: {fig_path}")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
