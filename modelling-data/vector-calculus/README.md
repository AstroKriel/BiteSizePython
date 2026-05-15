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

To evaluate the contraction, you first need all partial derivatives of all components: the gradient tensor `grad_b[j, i]` = d(b_j)/d(x_i).

`numpy.gradient` computes it one component at a time:

```python
for j in range(n_comp):
    grads = numpy.gradient(b[j], dx, dy)
    for i, g in enumerate(grads):
        grad_b[j, i] = g
```

---

## The contraction

With the gradient tensor in hand, the curvature is a sum over i at every grid point. For loops make this explicit:

```python
kappa = numpy.zeros_like(b)
for j in range(n_comp):
    for i in range(n_comp):
        kappa[j] += b[i] * grad_b[j, i]
```

`numpy.einsum` expresses the same thing in one line that mirrors the index notation directly:

```python
kappa = numpy.einsum("ixy,jixy->jxy", b, grad_b)
```

The string reads as: sum over `i`, keep `j`, `x`, `y`. Each letter maps to an axis. Repeated indices that do not appear in the output are contracted (summed). The result has the same shape as `b`.

See `before.py` and `after.py` for this in action.

---

## A note on accuracy

This is the naive approach. `numpy.gradient` drops to first-order accuracy at array boundaries, and periodic grids need boundary-aware stencils to stay second-order throughout. For production use, higher-order finite differences and proper boundary conditions improve accuracy considerably. The contraction itself is exact; the approximation lives entirely in how the gradient tensor is computed.
