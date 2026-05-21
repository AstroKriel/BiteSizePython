# finite differences

The derivative of a discretised field at a point is constructed by looking at how nearby samples compare. The more of the neighbouring field you use, the better the approximation.

## Depends on

- [`uv`](../../repo-setup/uv/)

---

## The minimal approximation

The simplest approach uses just two points: the value at the point and its right neighbour:

```
y'(x_i) ~ ( y_{i+1} - y_i ) / dx
```

This is first-order accurate: the error scales as O(dx). It only knows which direction the function moves, nothing about curvature or higher variation.

---

## Bringing in more of the neighbourhood

By averaging both a forward and backwards derivative (both of which are first order accurate), we can construct a second order centered difference:

```
y'(x_i) ~ 1/2 [( y_{i+1} - y_i ) / dx + ( y_i - y_{i-1} ) / dx]
        = ( y_{i+1} - y_{i-1} ) / (2 dx)
```

Continuing down this road, and reaching further out and using two neighbouring points on either side (making sure to weight them so the centre point cancels):

```
y'(x_i) ~ ( -y_{i+2} + 8 y_{i+1} - 8 y_{i-1} + y_{i-2} ) / (12 dx)
```

Similarly, for three neighbouring points on each side:

```
y'(x_i) ~ ( y_{i+3} - 9 y_{i+2} + 45 y_{i+1} - 45 y_{i-1} + 9 y_{i-2} - y_{i-3} ) / (60 dx)
```

As you will see in the example `script.py`, each layer of neighbours cancels another order of error, giving O(dx^4) and O(dx^6) respectively.

---

## Convergence

The payoff is easy to see in the convergence (right side) panel of `figures/convergence.png`: higher-order accurate methods can reach the same accuracy at far lower resolution than lower-order methods.

---

## Connection to 3D fields

Simulation grids are discretised fields. Taking a derivative along a grid axis is exactly the same operation: apply a stencil to the values at neighbouring grid points along that direction. The stencils, the convergence orders, and the accuracy tradeoffs are all identical. The only difference is that you have three axes to differentiate along instead of one.
