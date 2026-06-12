# type safety

Annotations guide you as you write your code; guards prevent misbehaviour.

## Depends on

- [`dependencies`](../../repo-setup/dependencies/)

---

## The problem

`before.py` is a normalisation pipeline: `compute_stats` returns the mean and standard deviation of an array; `normalise` shifts and scales the values. Two mistakes are hiding in it.

The first is in how `main` calls `normalise`. `compute_stats` returns a `tuple[float, float]`, but the call passes the whole tuple as the `mean` argument. Without annotations, nothing flags this at edit time. At runtime, numpy tries to subtract a 2-element tuple from an 8-element array and raises a shape error. The message says nothing about types; you are left to work backwards from a broadcasting failure to a wrong argument three lines earlier.

The second is in the data. When all input values are equal, `numpy.std` returns `0.0`, and `normalise` divides by it. No exception is raised; the result is `nan`. Your pipeline finishes without complaint.

These two mistakes are different in kind. The first is a type error: the wrong kind of value was passed. The second is a domain error: the right kind of value was passed, but its content violated an invariant the function depends on. Each needs a different fix.

---

## Annotations

A type annotation declares what a function accepts and returns. Pyright reads them without running the code and flags any call that violates the contract.

Here is `normalise` with annotations:

```python
def normalise(
    values: NDArray,
    mean: float,
    std: float,
) -> NDArray:
    return (values - mean) / std
```

Now pyright knows `mean` must be a `float`. The call in `before.py` that passes a tuple is immediately flagged:

```
error: Argument of type "tuple[float, float]" cannot be assigned to parameter "mean" of type "float"
```

The message names the type that was passed and the type that was expected. You see the mistake at the callsite, not wherever numpy eventually tried to use the result.

`NDArray` comes from `numpy.typing` and represents any NumPy array. Use it whenever a function expects numpy data rather than a plain Python list:

```python
from numpy.typing import NDArray
```

Try running pyright on the unannotated `before.py`:

```sh
uv run pyright before.py
```

Pyright reports no errors. Unannotated functions give it nothing to check; every call is acceptable. Now run it on `after.py`:

```sh
uv run pyright after.py
```

Zero errors. The annotated pipeline satisfies its own contracts.

---

## Guards

Pyright cannot know what values an array contains at a specific callsite. An array of identical values has the right type; its zero standard deviation is only discoverable when the code runs. A guard checks the invariant at the function boundary and raises a clear error before anything can go wrong downstream.

```python
def compute_stats(
    values: NDArray,
) -> tuple[float, float]:
    if values.size == 0:
        raise ValueError("`values` must not be empty.")
    std = float(numpy.std(values))
    if std == 0.0:
        raise ValueError("`values` has zero standard deviation; cannot normalise.")
    return float(numpy.mean(values)), std
```

A guard checks one condition and raises immediately. The error message names the parameter and says exactly what was wrong. Once `compute_stats` returns, you have a guarantee: the values are safe to normalise. `normalise` does not need to re-check.

---

## What each layer catches

| Mistake | Caught by |
|---|---|
| Passing a `tuple` where a `float` is expected | annotations + pyright |
| Passing a `list` where an `NDArray` is expected | annotations + pyright |
| Empty array | guard |
| Zero standard deviation | guard |

Neither layer replaces the other. Annotations cannot know what values an array holds at runtime; guards cannot flag a type mismatch at edit time. Together they stop mistakes at the earliest moment each is catchable.
