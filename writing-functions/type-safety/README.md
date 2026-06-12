# type safety

Type annotations guide you as you write your code; runtime guards prevent misbehaviour; unit tests confirm the results.

## Depends On

- [`dependencies`](../../repo-setup/dependencies/)
- [`unit-tests`](../unit-tests/)

---

## The Problem

Python is a dynamically typed language, which leads to minimal friction when starting your projects and cheap cost of experimenting with implementing ideas. Compared to working with a statically typed language like C++, Fortran, or Rust, this means:

- you do not declare variable types (in fact they can change in their lifetime), and there is no compilation step to enforce their type; the interpreter runs your code without checking
- functions work on any input that supports the required operations, regardless of its type

This same freedom can, however, become a burden as your project scales. Sometimes it shows up as a crash: a type mismatch can produce an error that points nowhere near the real cause. More dangerous are the cases where nothing crashes at all, and Python runs your code to completion with wrong results. For example:

- a `bool` added to an `int` is valid
- a `str` multiplied by an `int` is valid
- a `tuple` subtracted from an `NDArray` can silently broadcast into a plausible but wrong shape
- a function called with values that make its operation ill-defined produces `nan` or `inf` silently

In all of these cases, the code runs, and there are (incorrect) results, but you remain none the wiser. Three tools help, each working at a different layer.

---

## The Solutions

### Type Annotations

A type annotation declares the expected type of a value: a function's parameters, its return, or a variable at the point it is created. A static type checker reads them without running the code and flags any violation of the contract. In all lessons we use Pyright (see [`../pyright/`](../pyright/) for setup and configuration).

Annotating a variable is enough for Pyright to flag a wrong assignment:

```python
counts: dict[str, int] = {"apples": 3, "oranges": 1}
counts["bananas"] = "two"

labels: dict[str, str] = {"x": "time", "y": "distance"}
labels["z"] = 42
```

Here, Pyright knows the expected value types based on the annotation and flags at assignment, so `"two"` cannot be assigned to an `int` entry, and similarly `42` cannot be assigned to a `str` entry.

The same applies to functions. `NDArray` comes from `numpy.typing` and represents any NumPy array. Use it whenever a function expects numpy data rather than a plain Python list:

```python
from numpy.typing import NDArray

def compute_standardised_values(
    values: NDArray,
    mean_value: float,
    std_value: float,
) -> NDArray:
    return (values - mean_value) / std_value
```

Now Pyright knows `mean_value` must be a `float`, so, suppose you passed the full statistics tuple instead:

```python
stats = compute_stats(data)
standardised_values = compute_standardised_values(data, stats, 1.0)
```

where `stats` is a `(mean_value, std_value)` pair, Pyright will immediately flag:

```
error: Argument of type "tuple[float, float]" cannot be assigned to parameter "mean_value" of type "float"
```

The message names both the type that was received and the type that was expected. With this, you'll see the mistake at the callsite, and notibly, not wherever downstream numpy eventually tried to use the result.

Since `pyright` is a dependency in `pyproject.toml`, `uv` exposes the ability to check static typing:

```sh
uv run pyright script.py
```

For `script.py`, you should see zero errors. If a contract were violated anywhere in the script, Pyright would name the types involved and point to the exact callsite.

### Runtime Guards

Pyright can verify that an argument has the right type, but cannot inspect its value. This becomes an issue when the type is satisfied but the behaviour depends on the values. `compute_stats`, which we called earlier, requires `values` to be non-empty and to have a non-zero standard deviation; both are dynamically determined, not by the declared type alone, so Pyright cannot see them. A runtime guard catches each case at the function boundary and raises a clear error before anything can go wrong downstream.

```python
def compute_stats(
    values: NDArray,
) -> tuple[float, float]:
    if not isinstance(values, numpy.ndarray):
        raise TypeError("`values` must be an NDArray.")
    if values.size == 0:
        raise ValueError("`values` must not be empty.")
    std_value = float(numpy.std(values))
    if std_value == 0.0:
        raise ValueError("`values` has zero standard deviation; cannot normalise.")
    return float(numpy.mean(values)), std_value
```

Each guard checks one condition and raises immediately with a message naming the parameter and what was wrong. The first uses `isinstance` to enforce the type annotation at runtime; type annotations are not enforced by Python itself, and without it a caller could pass a wrong type undetected. Once `compute_stats` returns, you have a guarantee: the values are safe to standardise.

The same applies to `compute_standardised_values`, which can also be called directly without going through `compute_stats`. `isinstance` accepts a tuple of types, so `(float, numpy.floating)` covers both Python floats and NumPy scalar types like `float64`:

```python
def compute_standardised_values(
    values: NDArray,
    mean_value: float,
    std_value: float,
) -> NDArray:
    if not isinstance(values, numpy.ndarray):
        raise TypeError("`values` must be an NDArray.")
    if not isinstance(mean_value, (float, numpy.floating)):
        raise TypeError("`mean_value` must be a float.")
    if not isinstance(std_value, (float, numpy.floating)):
        raise TypeError("`std_value` must be a float.")
    if std_value == 0.0:
        raise ValueError("`std_value` must not be zero.")
    return (values - mean_value) / std_value
```

The final guard catches a zero `std_value` passed directly, bypassing the check in `compute_stats`.

### Unit Tests

Unit tests confirm that a function or workflow does what it is expected to do. They do not test how it is used; type annotations and runtime guards ensure it cannot be misused. See [`../unit-tests/`](../unit-tests/) for a full walkthrough.

---

## The Lesson: Try Breaking Something

**Type Annotations:** remove `: float` from `mean_value` in `compute_standardised_values`, then add this to `main`:

```python
stats = compute_stats(data)
compute_standardised_values(data, stats, 1.0)
```

Run `uv run pyright script.py`. Pyright reports nothing; without the annotation it has no contract to check against the call. Undo both changes and confirm zero errors.

**Runtime Guards:** remove the `if std_value == 0.0` check from `compute_stats`, then add this to `main`:

```python
flat_data = numpy.array([3.0, 3.0, 3.0, 3.0])
mean_value, std_value = compute_stats(flat_data)
print(compute_standardised_values(flat_data, mean_value, std_value))
```

Run `uv run script.py`. The script finishes without error; the output is `[nan nan nan nan]`. Undo both changes.

---

## In Summary

| Mistake | Caught by |
|---|---|
| Passing a `tuple` where a `float` is expected | type annotations + Pyright |
| Passing a `list` where an `NDArray` is expected | type annotations + Pyright |
| Empty array | runtime guard |
| Zero standard deviation | runtime guard |
| Incorrect result for valid inputs | unit tests |
| Edge case not handled correctly | unit tests |

Neither layer replaces the other. Type annotations cannot know what values an array holds at runtime; runtime guards cannot flag a type mismatch at edit time. Together they stop mistakes at the earliest moment each is catchable.
