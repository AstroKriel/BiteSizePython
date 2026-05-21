##
## === DEPENDENCIES
##

## stdlib
from pathlib import Path

## third-party
import numpy

## local
from local_helpers import pipeline_helpers

##
## === CONSTANTS
##

FIGURES_DIR = Path("figures")

##
## === CURVATURE
##


def compute_field_curvature(
    *,
    unit_vector_field: numpy.ndarray,
    gradient_tensor: numpy.ndarray,
) -> numpy.ndarray:
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
    return field_curvature


##
## === PROGRAM MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    pipeline_helpers.run_pipeline(
        compute_curvature_fn=compute_field_curvature,
        fig_path=FIGURES_DIR / "curvature_before.png",
    )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
