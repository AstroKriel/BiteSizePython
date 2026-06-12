# type safety

Annotations guide you as you write your code; guards prevent misbehaviour.

## Depends on

- [`dependencies`](../../repo-setup/dependencies/)

---

## The problem

Python is a dynamically typed language, which leads to minimal friction when starting your projects and cheap cost of experimenting with implementing ideas. Compared to working with a statically typed language like C++, Fortran, or Rust, this means:

- you do not declare variable types (in fact they can change in their lifetime), and there is no compilation step to enforce their type; the interpreter runs your code without checking
- functions work on any input that supports the required operations, regardless of its type

This same freedom can, however, become a burden as your project scales. Sometimes it shows up as a crash: a type mismatch can produce an error that points nowhere near the real cause. More dangerous are the cases where nothing crashes at all, and Python runs your code to completion with wrong results. For example:

- a `bool` added to an `int` is valid
- a `str` multiplied by an `int` is valid
- a `tuple` subtracted from an `NDArray` can silently broadcast into a plausible but wrong shape

In all of these cases, the code runs, there are (incorrect) results, but you remain none the wiser.

The lesson here is not to annotate and guard everything from the start; that would defeat the point of dynamic typing. The right moment to introduce guardrails is when you want to solidify behaviour: once a function's interface is settled, or once you are relying on a pipeline to produce results you trust. Annotations and guards are how you lock in decisions you have already made.

`normalise(data, stats, 1.0)` is a good example. It looks plausible: `stats` holds the statistics the function needs. What it needs specifically is a `float`; `stats` is a tuple. A compiler would refuse this. Python runs it, and when numpy eventually tries to subtract a tuple from an array, it raises a shape mismatch error with no mention of types.

```python
stats = compute_stats(data)
normalised = normalise(data, stats, 1.0)  ## stats is a (mean, std) pair; the error says shapes don't match
```

Type mistakes are one failure mode. Value mistakes are another, and no compiler catches them. An array of identical values has a standard deviation of zero, and dividing by zero in numpy does not raise an exception; it returns `nan`. Your pipeline finishes; the results look like numbers.

Both failure modes have an answer: annotations let a tool check types before your code runs; guards enforce value constraints when it does. This is what `before.py` and `after.py` show.

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
