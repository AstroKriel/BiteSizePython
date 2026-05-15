##
## === DEPENDENCIES
##

## stdlib
from pathlib import Path

## third-party
import matplotlib.pyplot as plt
import numpy

## local
from local_helpers.vector_field import (
    compute_gradient_tensor,
    make_vector_field,
    normalize_vector_field,
)

##
## === CONSTANTS
##

NUM_POINTS = 64
X_MIN, X_MAX = -numpy.pi, numpy.pi
Y_MIN, Y_MAX = -numpy.pi, numpy.pi
FIGURES_DIR = Path("figures")

##
## === MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
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
    grid_xs, grid_ys = numpy.meshgrid(position_x, position_y, indexing="ij")
    vector_field = make_vector_field(grid_xs, grid_ys)
    unit_vector_field = normalize_vector_field(vector_field)
    gradient_tensor = compute_gradient_tensor(unit_vector_field, cell_width_x, cell_width_y)
    ## kappa_j = v_i * d(v_j)/d(x_i), summed over dir_index
    num_comps = unit_vector_field.shape[0]
    num_cells_x, num_cells_y = unit_vector_field.shape[1], unit_vector_field.shape[2]
    field_curvature = numpy.zeros(
        shape=(num_comps, num_cells_x, num_cells_y),
    )
    for comp_index in range(num_comps):
        for dir_index in range(num_comps):
            field_curvature[comp_index] += unit_vector_field[dir_index] * gradient_tensor[
                comp_index,
                dir_index,
            ]
    field_curvature_magnitude = numpy.sqrt(
        numpy.sum(
            field_curvature**2,
            axis=0,
        ),
    )
    print(
        f"\t> curvature magnitude: min={field_curvature_magnitude.min():.4f}, max={field_curvature_magnitude.max():.4f}",
    )
    fig, ax = plt.subplots()
    im = ax.pcolormesh(grid_xs, grid_ys, field_curvature_magnitude, cmap="inferno")
    fig.colorbar(
        im,
        ax=ax,
        label=r"$|\kappa|$",
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig_path = FIGURES_DIR / "curvature_before.png"
    fig.savefig(fig_path, dpi=150)
    print(f"\t> saved: {fig_path}")


if __name__ == "__main__":
    main()
