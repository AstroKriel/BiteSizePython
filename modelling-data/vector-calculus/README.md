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
    field_comp = vector_field[comp_index]
    gradient_tensor[comp_index, 0] = (
        numpy.roll(field_comp, -1, axis=0) -
        numpy.roll(field_comp, +1, axis=0)
    ) / (2.0 * cell_width_x)
    gradient_tensor[comp_index, 1] = (
        numpy.roll(field_comp, -1, axis=1) -
        numpy.roll(field_comp, +1, axis=1)
    ) / (2.0 * cell_width_y)
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

---

## More examples of `einsum` in action

Curvature is just one contraction. Most vector-calculus operations are also index expressions, so the same `einsum` grammar can express them, whether they reduce, preserve, or raise the tensor-rank.

**Divergence** reuses the gradient tensor you already built. It is the trace `d(b_i)/d(x_i)`, summing the diagonal where component and direction match:

```python
## div b = d(b_i)/d(x_i): sum the diagonal of gradient_tensor[comp, dir]
div_field = numpy.einsum("iixy->xy", gradient_tensor)
```

A repeated index on a single input (`ii`) contracts it with itself, picking out and summing the diagonal to leave a scalar field.

**Dot products** combine two vector fields into a scalar field, `a_i b_i`:

```python
dot_field = numpy.einsum("ixy,ixy->xy", field_a, field_b)
```

Taking a field with itself gives its magnitude squared, `b_i b_i`, which is exactly the sum `normalize_vector_field` computes before it divides.

**Outer products** go the other way, building a tensor from two vectors, `a_i b_j`. A field combined with itself gives the tension (stress) dyad `b_i b_j`:

```python
## no index is summed, so rank goes up: the output keeps both i and j
tension_tensor = numpy.einsum("ixy,jxy->ijxy", vector_field, vector_field)
```

The rule for reading any string: an index on the inputs but not the output is summed (rank goes down, as in the dot product and divergence); an index kept on the output is not (rank preserved or raised, as in the outer product).

| operation | index notation | `einsum` |
|---|---|---|
| dot product | `a_i b_i` | `"ixy,ixy->xy"` |
| divergence | `d(b_i)/d(x_i)` | `"iixy->xy"` (on `gradient_tensor`) |
| transpose | `T_ij -> T_ji` | `"ijxy->jixy"` |
| outer product | `a_i b_j` | `"ixy,jxy->ijxy"` |
