# structured data

A dataclass makes the structure of your data explicit: named fields, optional immutability, built-in validation, and methods that travel with the object.

---

## Setup

We will demonstrate the utility of dataclasses through a problem you will run into often: fitting a model to data. `scipy.curve_fit` is a common tool for this, and its raw output is a good example of the kind of thing a dataclass is designed to improve.

---

## The problem

`curve_fit` returns `popt` and `pcov`: plain positional arrays. Parameter order follows your model function's argument list. If your model is `f(x, slope, intercept)` then `popt[0]` is slope and `popt[1]` is intercept. Get the order wrong and nothing tells you.

Every callsite has to carry that knowledge:

```python
print(f"slope: {popt[0]:.4f}")      # is popt[0] the slope?
print(f"intercept: {popt[1]:.4f}")  # only one way to find out
```

Every new reader has to look back at the model function to work it out. Tuples and dicts have the same problem in different ways: a tuple gives you no names at all, and a dict lets typos silently create new keys.

---

## The fix

Wrap the result once, at the source, in a dataclass. Index arithmetic happens once, in one place. After that, every callsite uses names:

```python
print(f"slope: {result.slope:.4f} +/- {result.slope_sigma:.4f}")
```

`LineFit.from_fit(data_series)` wraps the `curve_fit` call. Construction logic lives in one place, and the rest of the codebase never sees `popt`. It also uses `data_series.y_sigmas` as fit weights if provided, with no extra work at the callsite.

---

## Locking it in

A fit result is a fact about your data. `frozen=True` makes it immutable: any accidental assignment raises a `FrozenInstanceError` immediately rather than silently corrupting downstream analysis.

`__post_init__` runs immediately after construction. Use it when there is a meaningful invariant to check. For a fit result there is not much to check, but for the input data there is: all arrays must have the same length. A `DataSeries` dataclass validates this once at construction:

```python
def __post_init__(self) -> None:
    if len(self.x_values) != len(self.y_values):
        raise ValueError(...)
    if self.y_sigmas is not None and len(self.y_sigmas) != len(self.x_values):
        raise ValueError(...)
```

Once a `DataSeries` exists, it is guaranteed valid. `LineFit.from_fit` does not need to re-check. Neither does anything else downstream.

---

## What travels with the data

A dataclass is still a class. Methods are attached directly to the object and travel with it wherever it goes. No standalone helpers. No passing fields around separately.

```python
result.print_summary()
result.evaluate_at(x_values)
result.rms_residual(data_series)
```

See `before.py` and `after.py` for this in action.
