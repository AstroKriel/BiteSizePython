##
## === DEPENDENCIES
##

import numpy

from numpy.typing import NDArray

##
## === CONSTANTS
##

FORWARD = -1
BACKWARD = +1

##
## === FUNCTIONS
##


def create_vector_field(
    *,
    grid_xs: NDArray,
    grid_ys: NDArray,
) -> NDArray:
    return numpy.stack(
        [
            numpy.sin(grid_ys) + 1.5,
            numpy.cos(grid_xs) + 1.5,
        ],
        axis=0,
    )


def normalize_vector_field(
    *,
    vector_field: NDArray,
) -> NDArray:
    field_magnitude = numpy.sqrt(
        numpy.sum(
            vector_field**2,
            axis=0,
            keepdims=True,
        ),
    )
    return vector_field / field_magnitude


def compute_gradient_tensor(
    *,
    vector_field: NDArray,
    cell_width_x: float,
    cell_width_y: float,
) -> NDArray:
    num_comps = vector_field.shape[0]
    num_cells_x, num_cells_y = vector_field.shape[1], vector_field.shape[2]
    gradient_tensor = numpy.zeros(
        shape=(num_comps, num_comps, num_cells_x, num_cells_y),
    )
    for comp_index in range(num_comps):
        field = vector_field[comp_index]
        gradient_tensor[comp_index, 0] = (
            numpy.roll(field, int(1 * FORWARD), axis=0) -
            numpy.roll(field, int(1 * BACKWARD), axis=0)
        ) / (2.0 * cell_width_x)
        gradient_tensor[comp_index, 1] = (
            numpy.roll(field, int(1 * FORWARD), axis=1) -
            numpy.roll(field, int(1 * BACKWARD), axis=1)
        ) / (2.0 * cell_width_y)
    return gradient_tensor
