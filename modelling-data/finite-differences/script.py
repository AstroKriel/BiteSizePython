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

from matplotlib.axes import Axes as mpl_Axes
from numpy.typing import NDArray

##
## === CONSTANTS
##

X_MIN = 0.0
X_MAX = 2.0 * numpy.pi
PLANNED_NUM_POINTS = [10, 20, 50, 100, 200, 500, 1000]
FIGURES_DIR = Path("figures")

##
## === TEST FUNCTIONS
##


def compute_y_values(
    x_values: NDArray,
) -> NDArray:
    return numpy.sin(2.0 * x_values) + numpy.cos(x_values)


def compute_dydx_exact(
    x_values: NDArray,
) -> NDArray:
    return 2.0 * numpy.cos(2.0 * x_values) - numpy.sin(x_values)


##
## === STENCILS
##


def compute_1st_order_forward_difference(
    y_values: NDArray,
    *,
    cell_width: float,
) -> NDArray:
    return (y_values[1:] - y_values[:-1]) / cell_width


def compute_2nd_order_centered_difference(
    y_values: NDArray,
    *,
    cell_width: float,
) -> NDArray:
    return (y_values[2:] - y_values[:-2]) / (2.0 * cell_width)


def compute_4th_order_centered_difference(
    y_values: NDArray,
    *,
    cell_width: float,
) -> NDArray:
    numerator = (
        -y_values[4:]
        + 8.0 * y_values[3:-1]
        - 8.0 * y_values[1:-3]
        + y_values[:-4]
    )
    return numerator / (12.0 * cell_width)


def compute_6th_order_centered_difference(
    y_values: NDArray,
    *,
    cell_width: float,
) -> NDArray:
    numerator = (
        y_values[6:]
        - 9.0 * y_values[5:-1]
        + 45.0 * y_values[4:-2]
        - 45.0 * y_values[2:-4]
        + 9.0 * y_values[1:-5]
        - y_values[:-6]
    )
    return numerator / (60.0 * cell_width)


##
## === GRAD METHOD
##


@dataclass(frozen=True)
class Method:
    name: str
    compute_fn: Callable[..., NDArray]
    order: int
    x_slice: slice
    color: str


METHODS = [
    Method(
        name=r"forward $O(h)$",
        compute_fn=compute_1st_order_forward_difference,
        order=1,
        x_slice=slice(None, -1),
        color="blue",
    ),
    Method(
        name=r"centered $O(h^2)$",
        compute_fn=compute_2nd_order_centered_difference,
        order=2,
        x_slice=slice(1, -1),
        color="orange",
    ),
    Method(
        name=r"centered $O(h^4)$",
        compute_fn=compute_4th_order_centered_difference,
        order=4,
        x_slice=slice(2, -2),
        color="green",
    ),
    Method(
        name=r"centered $O(h^6)$",
        compute_fn=compute_6th_order_centered_difference,
        order=6,
        x_slice=slice(3, -3),
        color="red",
    ),
]

##
## === RMS ERROR
##


def compute_rms_error(
    method: Method,
    *,
    num_points: int,
) -> tuple[float, float]:
    x_values = numpy.linspace(
        start=X_MIN,
        stop=X_MAX,
        num=num_points,
        endpoint=False,
    )
    cell_width = float(x_values[1] - x_values[0])
    y_values = compute_y_values(x_values)
    dydx_approx = method.compute_fn(
        y_values,
        cell_width=cell_width,
    )
    dydx_exact = compute_dydx_exact(x_values[method.x_slice])
    rms_error = float(numpy.sqrt(numpy.mean((dydx_approx - dydx_exact) ** 2)))
    return cell_width, rms_error


##
## === PLOT HELPERS
##


def plot_derivative_approx(
    ax: mpl_Axes,
    *,
    x_values_exact: NDArray,
    dydx_values_exact: NDArray,
    x_values_approx: NDArray,
    y_values_approx: NDArray,
    cell_width_approx: float,
) -> None:
    ax.plot(
        x_values_exact,
        dydx_values_exact,
        color="black",
        zorder=5,
    )
    for method in METHODS:
        dydx_approx = method.compute_fn(
            y_values_approx,
            cell_width=cell_width_approx,
        )
        ax.plot(
            x_values_approx[method.x_slice],
            dydx_approx,
            marker="o",
            linestyle="none",
            markersize=6,
            color=method.color,
            label=method.name,
        )
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"${\rm d}y/{\rm d}x$")
    ax.legend(fontsize=8)


def plot_convergence(
    ax: mpl_Axes,
) -> None:
    for method in METHODS:
        inv_dx_values = []
        rms_errors = []
        for num_points in PLANNED_NUM_POINTS:
            cell_width, rms_error = compute_rms_error(
                method,
                num_points=num_points,
            )
            inv_dx_values.append(1.0 / cell_width)
            rms_errors.append(rms_error)
        inv_dx_arr = numpy.array(inv_dx_values)
        rms_errors_arr = numpy.array(rms_errors)
        ax.plot(
            inv_dx_arr,
            rms_errors_arr,
            marker="o",
            linestyle="none",
            markersize=6,
            color=method.color,
        )
        inv_dx_ref = numpy.array([inv_dx_arr[0], inv_dx_arr[-1]])
        rms_errors_ref = rms_errors_arr[0] * (inv_dx_ref / inv_dx_ref[0]) ** (-method.order)
        ax.plot(
            inv_dx_ref,
            rms_errors_ref,
            linestyle="--",
            alpha=0.4,
            color=method.color,
            label=rf"$O(h^{{{method.order}}})$",
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$1 / \Delta x$")
    ax.set_ylabel(r"$(N)^{-1/2} \sum_{i=1}^N (y_i - y_i^*)^{1/2}$")
    ax.legend(fontsize=8)


##
## === PROGRAM MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    x_values_exact = numpy.linspace(
        start=X_MIN,
        stop=X_MAX,
        num=500,
    )
    dydx_values_exact = compute_dydx_exact(x_values_exact)
    x_values_approx = numpy.linspace(
        start=X_MIN,
        stop=X_MAX,
        num=20,
        endpoint=False,
    )
    cell_width_approx = float(x_values_approx[1] - x_values_approx[0])
    y_values_approx = compute_y_values(x_values_approx)
    for method in METHODS:
        for num_points in PLANNED_NUM_POINTS:
            cell_width, rms_error = compute_rms_error(
                method,
                num_points=num_points,
            )
            print(f"\t> {method.name}: n={num_points}, dx={cell_width:.4f}, rms={rms_error:.2e}")
    fig, axes = mpl_plot.subplots(
        nrows=1,
        ncols=2,
        figsize=(10, 4),
    )
    plot_derivative_approx(
        axes[0],
        x_values_exact=x_values_exact,
        dydx_values_exact=dydx_values_exact,
        x_values_approx=x_values_approx,
        y_values_approx=y_values_approx,
        cell_width_approx=cell_width_approx,
    )
    plot_convergence(axes[1])
    fig.tight_layout()
    fig_path = FIGURES_DIR / "convergence.png"
    fig.savefig(
        fname=fig_path,
        dpi=150,
        bbox_inches="tight",
    )
    print(f"\t> saved: {fig_path}")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
