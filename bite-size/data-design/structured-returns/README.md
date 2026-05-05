# Structured Returns

Named fields mean you never guess argument order, and you can catch typos at definition time. See `before.py` and `after.py` for this in action.

---

## The Problem

There are three common ways to return several values from a function. Each with their own failure mode.

**Tuple or list:** the call site carries no information about what each value means. Was `p50_value` third or fourth? Was `min_value` first or last? Get it wrong and nothing will tell you; the code continues running.

**Dict:** positional problems are gone, but you have to remember the key name exactly. A typo either raises a `KeyError`, or, when assigning, silently creates a **new** key with no error at all.

---

## The Fix

A **dataclass** is a class where you declare the fields and Python generates `__init__`, `__repr__`, and equality for you. Use it as a return type and the call site becomes self-documenting.

```python
stats.p50_val  # AttributeError immediately; a typo cannot silently return wrong data
```

---

## Supercharged: Immutability

Add `frozen=True` and the dataclass becomes immutable after construction. Fields cannot be overwritten by accident.

```python
stats.p50_value = 0.0  # FrozenInstanceError; the object is read-only
```

---

## Supercharged: Validation

Define `__post_init__` and it runs immediately after construction. Bad data is caught before the object is ever returned or used downstream.

---

## Supercharged: Methods

A dataclass is still a class. Methods travel with the data wherever it goes; no passing fields around separately, no standalone helpers that take five arguments.

---

## Supercharged: Type-Checker Aware

Because the return type is a concrete named class, the type checker knows exactly which attributes exist. Tab completion and typo detection follow automatically. A `dict[str, float]` return gives the type checker nothing to work with.
