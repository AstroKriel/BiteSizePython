# finite differences

The derivative of a discretised field at a point is constructed by looking at how nearby samples compare. The more of the neighbouring field you use, the better the approximation.

## Depends on

- [`dependencies`](../../repo-setup/dependencies/)
- [`structured-data`](../structured-data/)

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

Continuing down this road and reaching further out, with two neighbouring points on either side, buys another two orders:

```
y'(x_i) ~ ( -y_{i+2} + 8 y_{i+1} - 8 y_{i-1} + y_{i-2} ) / (12 dx)
```

Similarly, three neighbouring points on each side gives us the sixth-order centered difference stencil:

```
y'(x_i) ~ ( y_{i+3} - 9 y_{i+2} + 45 y_{i+1} - 45 y_{i-1} + 9 y_{i-2} - y_{i-3} ) / (60 dx)
```

As you will see in the example `script.py`, each layer of neighbours cancels another order of error, giving O(dx^4) and O(dx^6) respectively.

---

## Convergence

The payoff is easy to see in the convergence (right side) panel of `figures/convergence.png`: higher-order accurate methods can reach the same accuracy at far lower resolution than lower-order methods.

The left panel of `figures/convergence.png` overlays each stencil's `dydx_approx` (coloured markers) on the exact derivative `dydx_exact` (black line) at a fixed, deliberately coarse resolution. Even with only a handful of points, the higher-order markers sit closer to the exact curve, while the first-order forward difference visibly lags.

---

## Extending to 3D fields

Simulation grids are often 3D discretised domains of various kinds of fields. Taking derivatives along any spatial axis is exactly the same operation as what we covered: apply a stencil to the values at neighbouring grid points along the desired spatial direction. The implementation extends just as directly. The only change is to pass an `axis` argument to `numpy.roll`, telling it which axis to shift along. That axis is exactly the direction you are differentiating. The 1D calls in `script.py` leave it unset (there is only one axis); for a 3D field you simply name the axis:

```python
## d/dx : shift along axis 0
numpy.roll(
    field,
    shift=int(1 * FORWARD),
    axis=0,
)

## d/dy : shift along axis 1
numpy.roll(
    field,
    shift=int(1 * FORWARD),
    axis=1,
)

## d/dz : shift along axis 2
numpy.roll(
    field,
    shift=int(1 * FORWARD),
    axis=2,
)
```

Every stencil in this lesson works unchanged on a 3D array this way: pass `axis=k` to each `numpy.roll`, and the same expression returns the derivative along axis `k`.
