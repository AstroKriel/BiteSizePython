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
    ## kappa_j = v_i * d(v_j)/d(x_i): "ixy,jixy->jxy" sums over dir_index, keeps comp_index, x, y
    return numpy.einsum("ixy,jixy->jxy", unit_vector_field, gradient_tensor)


##
## === PROGRAM MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    pipeline_helpers.run_pipeline(
        compute_curvature_fn=compute_field_curvature,
        fig_path=FIGURES_DIR / "curvature_after.png",
    )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
