# finite differences

A simulation gives you a field sampled on a grid. Finite differences give you its derivatives.

## Depends on

- [`uv`](../../repo-setup/uv/)

---

## The idea

Given values of a function at discrete points, the centered finite difference approximates the derivative at each point:

```
df/dx ≈ (f(x + h) - f(x - h)) / (2h)
```

The error shrinks as h². Halve the grid spacing, and the error drops by a factor of four.

`numpy.gradient` computes this across an entire array in one call:

```python
df_numerical = numpy.gradient(y, dx)
```

It uses second-order centered differences in the interior and first-order at the boundaries.

---

## Convergence

A numerical method is only trustworthy if it converges at the expected rate. The recipe:

1. Compute the numerical derivative at several grid resolutions
2. Compute the RMS error against the analytical derivative at each resolution
3. Confirm the error scales as h² on a log-log plot

```python
rms_error = float(numpy.sqrt(numpy.mean((df_numerical - df_exact) ** 2)))
```

If the slope on the log-log plot matches the expected order, the method is working correctly. If it does not, something is wrong.

See `script.py` for this in action.
