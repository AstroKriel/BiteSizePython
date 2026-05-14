# Structured Returns: Fitting

`scipy.curve_fit` gives you a positional array. A dataclass gives everyone else named fields.

---

## The Problem

`curve_fit` returns `popt`, a plain array where parameter order matches your model function's argument list. If your model is `f(x, slope, intercept)` then `popt[0]` is slope and `popt[1]` is intercept. Get the order wrong and nothing tells you.

Every callsite has to carry that knowledge. Every new reader has to go back to the model function to figure it out.

```python
print(f"slope:     {popt[0]:.4f}")  # is this right?
print(f"intercept: {popt[1]:.4f}")  # only one way to find out
```

Uncertainties make it worse: `numpy.sqrt(numpy.diag(pcov))` gives you another positional array in the same order.

---

## The Fix

Wrap the result once, at the source. Think about index order exactly once, in the wrapper function. After that, every callsite uses names.

```python
@dataclass(frozen=True)
class LineFit:
    slope: float
    intercept: float
    slope_sigma: float
    intercept_sigma: float
```

```python
result = fit_line(x, y)
print(f"slope: {result.slope:.4f} +/- {result.slope_sigma:.4f}")
```

See `before.py` and `after.py` for this in action.

---

## Why `frozen=True`

A fit result is a fact about your data. It should not change after construction. `frozen=True` makes it immutable: any accidental assignment raises a `FrozenInstanceError` immediately rather than silently corrupting downstream analysis.

---

## At Scale

Models with more parameters (amplitude, centre, width, baseline) benefit even more. The index arithmetic happens once, in one place, and the rest of the codebase never sees it.
