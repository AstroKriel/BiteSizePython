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

In all of these cases, the code runs, and there are (incorrect) results, but you remain none the wiser. Three tools help, each working at a different layer.

---

## Type Annotations

A type annotation declares the expected type of a value: a function's parameters, its return, or a variable at the point it is created. A static type checker reads them without running the code and flags any violation of the contract. In all lessons we use Pyright (see [`../pyright/`](../pyright/) for setup and configuration).

Annotating a variable is enough for Pyright to flag a wrong assignment:

```python
counts: dict[str, int] = {"apples": 3, "oranges": 1}
counts["bananas"] = "two"

labels: dict[str, str] = {"x": "time (s)", "y": "distance (m)"}
labels["z"] = 42
```

Here, Pyright knows the expected value types based on the annotation and flags at assignment, so `"two"` cannot be assigned to an `int` entry, and similarly `42` cannot be assigned to a `str` entry.

The same applies to functions. Here is `compute_standardised_values` with annotations:

```python
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

where `stats` is a `(mean_value, std_value)` pair, Pyright will immediately flag this:

```
error: Argument of type "tuple[float, float]" cannot be assigned to parameter "mean_value" of type "float"
```

The message names the type that was passed and the type that was expected. You see the mistake at the callsite, not wherever numpy eventually tried to use the result.

`NDArray` comes from `numpy.typing` and represents any NumPy array. Use it whenever a function expects numpy data rather than a plain Python list:

```python
from numpy.typing import NDArray
```

Run Pyright to check the whole script against its annotations:

```sh
uv run pyright script.py
```

Zero errors. Every call satisfies its contracts.

---

## Runtime Guards

Pyright cannot know what values an array contains at a specific callsite. An array of identical values has the right type; its zero standard deviation is only discoverable when the code runs. A guard checks the invariant at the function boundary and raises a clear error before anything can go wrong downstream.

```python
def compute_stats(
    values: NDArray,
) -> tuple[float, float]:
    if values.size == 0:
        raise ValueError("`values` must not be empty.")
    std_value = float(numpy.std(values))
    if std_value == 0.0:
        raise ValueError("`values` has zero standard deviation; cannot normalise.")
    return float(numpy.mean(values)), std_value
```

A guard checks one condition and raises immediately. The error message names the parameter and says exactly what was wrong. Once `compute_stats` returns, you have a guarantee: the values are safe to standardise. `compute_standardised_values` does not need to re-check.

---

## Unit Tests

A unit test confirms that a function returns the expected output for a given input. Write them for settled behaviour: the happy path, edge cases, and any guarantees the rest of your code relies on. They cannot catch a wrong type at the callsite or stop an invalid value from entering a function; that is the job of type annotations and runtime guards. See [`../unit-tests/`](../unit-tests/) for a full walkthrough.

---

## Try Breaking Something

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

## What Each Layer Catches

| Mistake | Caught by |
|---|---|
| Passing a `tuple` where a `float` is expected | type annotations + Pyright |
| Passing a `list` where an `NDArray` is expected | type annotations + Pyright |
| Empty array | runtime guard |
| Zero standard deviation | runtime guard |

Neither layer replaces the other. Type annotations cannot know what values an array holds at runtime; runtime guards cannot flag a type mismatch at edit time. Together they stop mistakes at the earliest moment each is catchable.
