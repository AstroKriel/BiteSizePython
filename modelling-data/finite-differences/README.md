# finite differences

The derivative of a discretised field at a point is constructed by looking at how nearby samples compare. The more of the neighbouring field you use, the better the approximation.

## Depends on

- [`uv`](../../repo-setup/uv/)

---

## The minimal approximation

The simplest approach uses just two points: the value at the point and its right neighbour:

```
f'(x_i) ≈ ( f_{i+1} - f_i ) / h
```

This is first-order accurate: the error scales as O(h). It only knows which direction the function moves, nothing about curvature or higher variation.

---

## Bringing in more of the neighbourhood

Looking symmetrically at both sides immediately improves accuracy, because the left and right neighbours together say something about curvature that a one-sided difference cannot:

```
f'(x_i) ≈ ( f_{i+1} - f_{i-1} ) / (2h)
```

This is second-order accurate: O(h²). Reaching further out adds more information about how the function varies, and each additional layer of neighbours buys another order:

**4th order**, two neighbours on each side:

```
f'(x_i) ≈ ( -f_{i+2} + 8 f_{i+1} - 8 f_{i-1} + f_{i-2} ) / (12h)
```

**6th order**, three neighbours on each side:

```
f'(x_i) ≈ ( f_{i+3} - 9 f_{i+2} + 45 f_{i+1} - 45 f_{i-1} + 9 f_{i-2} - f_{i-3} ) / (60h)
```

Halving h reduces the error by 2^n for an n-th order method.

---

## Convergence

The payoff is visible on a log-log convergence plot. Each method falls on a straight line whose slope is its order. Higher-order methods need far fewer grid points to reach the same accuracy.

`script.py` tests all four methods on `f(x) = sin(2x) + cos(x)` and produces a two-panel figure: the derivative approximations at a coarse grid, and the convergence of each method across grid resolutions.

---

## Connection to 3D fields

Simulation grids are discretised fields. Taking a derivative along a grid axis is exactly the same operation: apply a stencil to the values at neighbouring grid points along that direction. The stencils, the convergence orders, and the accuracy tradeoffs are all identical. The only difference is that you have three axes to differentiate along instead of one.
