##
## === DEPENDENCIES
##

## stdlib
from pathlib import Path
from typing import Callable

## third-party
import matplotlib.pyplot as mpl_plot
import numpy

## local
from local_helpers import field_helpers

##
## === CONSTANTS
##

NUM_POINTS = 64
X_MIN, X_MAX = -numpy.pi, numpy.pi
Y_MIN, Y_MAX = -numpy.pi, numpy.pi

##
## === PIPELINE
##


def run_pipeline(
    *,
    compute_curvature_fn: Callable[..., numpy.ndarray],
    fig_path: Path,
) -> None:
    position_x = numpy.linspace(
        start=X_MIN,
        stop=X_MAX,
        num=NUM_POINTS,
        endpoint=False,
    )
    position_y = numpy.linspace(
        start=Y_MIN,
        stop=Y_MAX,
        num=NUM_POINTS,
        endpoint=False,
    )
    cell_width_x = float(position_x[1] - position_x[0])
    cell_width_y = float(position_y[1] - position_y[0])
    grid_xs, grid_ys = numpy.meshgrid(
        position_x,
        position_y,
        indexing="ij",
    )
    vector_field = field_helpers.create_vector_field(
        grid_xs=grid_xs,
        grid_ys=grid_ys,
    )
    unit_vector_field = field_helpers.normalize_vector_field(
        vector_field=vector_field,
    )
    gradient_tensor = field_helpers.compute_gradient_tensor(
        vector_field=unit_vector_field,
        cell_width_x=cell_width_x,
        cell_width_y=cell_width_y,
    )
    field_curvature = compute_curvature_fn(
        unit_vector_field=unit_vector_field,
        gradient_tensor=gradient_tensor,
    )
    field_curvature_magnitude = numpy.sqrt(
        numpy.sum(
            field_curvature**2,
            axis=0,
        ),
    )
    print(
        f"\t> curvature magnitude: min={field_curvature_magnitude.min():.4f}, max={field_curvature_magnitude.max():.4f}",
    )
    fig, ax = mpl_plot.subplots()
    mesh = ax.pcolormesh(
        grid_xs,
        grid_ys,
        field_curvature_magnitude,
        cmap="inferno",
    )
    fig.colorbar(
        mesh,
        ax=ax,
        label=r"field-line curvature",
    )
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    fig.tight_layout()
    fig.savefig(fig_path)
    print(f"\t> saved: {fig_path}")
