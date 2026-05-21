# structured data

A dataclass makes the structure of your data explicit: named fields, optional immutability, built-in validation, and methods that travel with the object.

## Depends on

- [`dependencies`](../../repo-setup/dependencies/)

---

## The problem

As projects grow, you make decisions early that you have to remember later. `scipy.curve_fit` is a good example of where this comes up; it returns the fitted parameters `popt` and covariance matrix `pcov` as plain positional arrays. Extracting useful values requires you to know the order of parameters in your model, which is easy to remember when you write it, but much harder many weeks later, and that friction adds up.

```python
popt, pcov = curve_fit(...)
print(f"slope: {popt[0]:.4f}")  # is popt[0] the slope or intercept?
```

Every new reader has to look back at the model function to work it out. Tuples and dicts have the same problem in different ways: a tuple gives you no names at all, and a dict lets typos silently create new keys. This is what `before.py` shows.

---

## The fix

Wrap the result once, at the source, in a dataclass. Index arithmetic happens once, in one place. After that, every callsite uses names:

```python
print(f"slope: {result.slope:.4f} +/- {result.slope_sigma:.4f}")
```

In `after.py`, `LineFit.from_fit(data_series)` wraps the `curve_fit` call. Construction logic lives in one place, and the rest of the codebase never sees `popt`.

---

## Locking it in

`after.py` defines two dataclasses: `DataSeries` for the input data and `LineFit` for the result. Both use `frozen=True`, making them immutable: any accidental assignment raises a `FrozenInstanceError` immediately rather than silently corrupting downstream analysis.

`DataSeries` makes use of the `__post_init__` routine that runs automnatically after construction (this method is empty by default). Overwrite it when there is a meaningful invariant to validate. For `LineFit` there is no such invariant to check, but there is for `DataSeries`: all data arrays must have the same length:

```python
def __post_init__(self) -> None:
    if len(self.x_values) != len(self.y_values):
        raise ValueError(...)
    if self.y_sigmas is not None and len(self.y_sigmas) != len(self.x_values):
        raise ValueError(...)
```

Once a `DataSeries` exists, it is guaranteed valid. `LineFit.from_fit` does not need to re-check. Neither does anything else downstream. It also uses `data_series.y_sigmas` as fit weights if provided, with no extra work at the callsite.

---

## What travels with the data

A dataclass is a class designed to hold structured data. By default it gives you automatic construction from named fields and equality comparison between instances. On top of that, you can opt in to immutability with `frozen=True` and define a `__post_init__` hook to validate the data at construction time. Like with classes, you can attach methods to the dataclass, which will travel with the object wherever it goes:

```python
result = LineFit.from_fit(data_series=data_series)
result.print_summary()
result.evaluate_at(x_values)
result.rms_residual
```

See `before.py` and `after.py` for this in action.
