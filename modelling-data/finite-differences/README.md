# finite differences

A derivative at a grid point can be approximated from nearby function values. The accuracy depends on how many neighbours you use and how you combine them.

## Depends on

- [`uv`](../../repo-setup/uv/)

---

## The stencil

A stencil is a fixed pattern of indices centred on a grid point. Each stencil gives a different approximation for the derivative at that point. The coefficients are chosen to cancel as many Taylor series terms as possible. The more you cancel, the higher the convergence order.

---

## Forward difference

Uses two grid points — the point and its right neighbour:

```
f'(x_i) ≈ ( f_{i+1} - f_i ) / h
```

First-order accurate: error scales as O(h). Halve the grid spacing, halve the error.

---

## Centered differences

Symmetric stencils cancel the even-order Taylor terms automatically. A wider stencil cancels more terms and buys a higher order.

**2nd order** — one neighbour on each side:

```
f'(x_i) ≈ ( f_{i+1} - f_{i-1} ) / (2h)
```

**4th order** — two neighbours on each side:

```
f'(x_i) ≈ ( -f_{i+2} + 8 f_{i+1} - 8 f_{i-1} + f_{i-2} ) / (12h)
```

**6th order** — three neighbours on each side:

```
f'(x_i) ≈ ( f_{i+3} - 9 f_{i+2} + 45 f_{i+1} - 45 f_{i-1} + 9 f_{i-2} - f_{i-3} ) / (60h)
```

Halving h reduces the error by 2^n for an n-th order method.

---

## Convergence

To verify a method, vary the grid spacing and measure the RMS error against the exact derivative. On a log-log plot, an n-th order method falls on a straight line with slope n.

`script.py` tests all four methods on `f(x) = sin(2x) + cos(x)` and produces a 2x2 figure:

- **function** — the test function on a fine grid
- **derivative approximations** — each method overlaid on the exact derivative at a coarse grid
- **convergence** — RMS error vs grid spacing on a log-log scale, with expected slope references
- **pointwise error** — absolute error at each grid point for the coarse example
