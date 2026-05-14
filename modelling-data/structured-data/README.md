# structured data

Build context into the object. Everything the data needs, the object carries.

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

## Named fields

A `dataclass` wraps the result once, at the source. Index arithmetic happens once, in one place. After that, every callsite uses names:

```python
print(f"slope: {result.slope:.4f} +/- {result.slope_sigma:.4f}")
```

---

## Immutability

A fit result is a fact about your data. `frozen=True` makes it immutable: any accidental assignment raises a `FrozenInstanceError` immediately rather than silently corrupting downstream analysis.

---

## Validation

`__post_init__` runs immediately after construction. Bad data is caught before the object is ever returned or used downstream:

```python
def __post_init__(self) -> None:
    if self.slope_sigma <= 0.0 or self.intercept_sigma <= 0.0:
        raise ValueError(...)
```

---

## Attached methods

A dataclass is still a class. Methods travel with the data wherever it goes. No standalone helpers. No passing fields around separately.

```python
result.print_summary()
result.evaluate_at(x_values)
result.rms_residual(x_ref, y_ref)
```

---

## The factory classmethod

`LineFit.from_fit(x_values, y_values)` wraps the `curve_fit` call. Construction logic lives in one place. After that, the rest of the codebase never sees `popt`.

See `before.py` and `after.py` for this in action.
