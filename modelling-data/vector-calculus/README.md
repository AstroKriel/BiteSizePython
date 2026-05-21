# vector calculus

Index notation is the most convenient language for analytic vector calculus. `numpy.einsum` brings this same language to computational vector calculus in Python.

## Depends on

- [`dependencies`](../../repo-setup/dependencies/)
- [`project-layout`](../../repo-setup/project-layout/)
- [`finite-differences`](../finite-differences/)

---

## The curvature vector

The directional derivative of a unit vector field b along itself gives the curvature vector:

```
kappa_j = b_i * d(b_j)/d(x_i)
```

The index i is summed over (Einstein convention). At each point in space, this tells you how fast b is turning and in which direction.

---

## The gradient tensor

To evaluate the contraction, you first need all partial derivatives of all components: the gradient tensor `gradient_tensor[comp_index, dir_index]` = d(b_comp)/d(x_dir).

We sample the domain with `endpoint=False`, so the grid is periodic: the cell after the last one wraps back to the first. This means the second-order centered difference stencil from the [finite-differences](../finite-differences/) lesson applies everywhere, including at the boundaries. `numpy.roll` implements the wrap:

```python
for comp_index in range(num_comps):
    field = vector_field[comp_index]
    gradient_tensor[comp_index, 0] = (numpy.roll(field, -1, axis=0) -
                                      numpy.roll(field, 1, axis=0)) / (2.0 * cell_width_x)
    gradient_tensor[comp_index, 1] = (numpy.roll(field, -1, axis=1) -
                                      numpy.roll(field, 1, axis=1)) / (2.0 * cell_width_y)
```

Each `roll(..., -1)` shifts the array one step forward; `roll(..., 1)` shifts it one step backward. Their difference divided by `2h` gives the centered derivative at every cell with uniform second-order accuracy.

---

## The contraction

With the gradient tensor in hand, the curvature is a sum over i at every grid point. For loops make this explicit:

```python
field_curvature = numpy.zeros_like(unit_vector_field)
for comp_index in range(num_comps):
    for dir_index in range(num_comps):
        field_curvature[comp_index] += unit_vector_field[dir_index] * gradient_tensor[comp_index, dir_index]
```

`numpy.einsum` expresses the same thing in one line that mirrors the index notation directly:

```python
field_curvature = numpy.einsum("ixy,jixy->jxy", unit_vector_field, gradient_tensor)
```

The string reads as: sum over `i`, keep `j`, `x`, `y`. Each letter maps to an axis. Repeated indices that do not appear in the output are contracted (summed). The result has the same shape as `unit_vector_field`.

See `before.py` and `after.py` for this in action.
