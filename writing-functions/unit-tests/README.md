# unit tests

A unit test is a small, fast check that pins one behaviour of one function. Run the whole suite after any change and a broken behaviour announces itself immediately, before the mistake flows downstream and corrupts a result you trusted.

## Depends on

- [`dependencies`](../../repo-setup/dependencies/)
- [`project-layout`](../../repo-setup/project-layout/)

---

## The layout

The code under test lives in `src/local_helpers/`, split into small modules:

```
src/local_helpers/
    arrays.py       # numeric array helpers
    sequences.py    # list helpers
    validation.py   # input guards
```

The tests live in `utests/`, mirroring that structure, one `test_<module>.py` per module:

```
utests/
    test_arrays.py
    test_sequences.py
    test_validation.py
```

You do not register these files anywhere. `pyproject.toml` points `pytest` at the folder, and it discovers every `test_*.py` for you:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]   # make src/ importable without installing the package
testpaths = ["utests"] # where pytest looks for test files
```

`pytest` is listed as a development-only dependency, separate from the package's real dependencies: it is needed to *test* the code, not to *run* it. `uv` installs it for you anyway, so the whole interface is one command:

```sh
uv run pytest
```

You should see every test pass.

---

## Anatomy of a test

Each test is a method on a `unittest.TestCase` class. The method name says what behaviour it checks, and the body follows the same three beats every time: build the input, call the function, assert on the result.

```python
class TestNormalise(unittest.TestCase):

    def test_maps_to_unit_range(
        self,
    ) -> None:
        result = arrays.normalise(
            numpy.array([2.0, 4.0, 6.0]),
        )
        numpy.testing.assert_array_almost_equal(
            result,
            [0.0, 0.5, 1.0],
        )
```

A test class groups the checks for one function; a test method is one behaviour. When a method fails, its name alone tells you what broke.

---

## Different checks for different abilities

Each module is paired with the kind of assertion that fits what it does. Reach for the one that matches the ability you are pinning:

- **`test_arrays.py` -> floating-point results.** Never compare floats with `==`; rounding makes that brittle. Use `numpy.testing.assert_array_almost_equal` for arrays, and `assertTrue(numpy.isnan(...))` to pin the `nan` that `safe_log10` returns for non-positive inputs.
- **`test_sequences.py` -> exact results.** Lists of integers have one right answer, so `assertEqual` compares them directly, element for element.
- **`test_validation.py` -> raised errors.** A guard's job is to *reject* bad input, so the behaviour under test is the exception itself. `with self.assertRaises(ValueError):` passes only when the call raises.

---

## Try breaking something

The fastest way to see what each assertion guards is to break the thing it guards:

1. Open `src/local_helpers/arrays.py` and change `normalise` to divide by `largest` instead of `largest - smallest`.
2. Run `uv run pytest`.
3. `test_maps_to_unit_range` fails, and the report shows the expected values next to the wrong ones.
4. Undo the change and watch it pass again.

Repeat with the others: drop the `raise` in `require_positive` and `test_zero_raises` fails; return the wrong slice from `chunk` and `assertEqual` flags the mismatch. The test that fails points straight at the ability you broke.

---

## Unit tests vs validation tests

Unit tests are fast and deterministic: a fixed input has a single known answer. Some properties do not fit that mould, such as "does this method converge at the expected rate?", where the answer is a trend across resolutions rather than a single value. Those belong in a separate *validation* test; the convergence check in the [`finite-differences`](../../modelling-data/finite-differences/) lesson is exactly that kind of test.
