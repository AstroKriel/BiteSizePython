# vector calculus

The curvature of a vector field measures how quickly field lines bend. Computing it requires a tensor contraction that einsum handles in one line.

## Depends on

- [`uv`](../../repo-setup/uv/)
- [`project-structure`](../../repo-setup/project-structure/)
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

`numpy.gradient` computes it one component at a time:

```python
for comp_index in range(num_comps):
    field_gradients = numpy.gradient(unit_vector_field[comp_index], cell_width_x, cell_width_y)
    for dir_index, field_gradient in enumerate(field_gradients):
        gradient_tensor[comp_index, dir_index] = field_gradient
```

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

---

## A note on accuracy

This is the naive approach. `numpy.gradient` drops to first-order accuracy at array boundaries, and periodic grids need boundary-aware stencils to stay second-order throughout. For production use, higher-order finite differences and proper boundary conditions improve accuracy considerably. The contraction itself is exact; the approximation lives entirely in how the gradient tensor is computed.
