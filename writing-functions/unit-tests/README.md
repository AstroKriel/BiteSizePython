# unit tests

Unit tests pin expected behaviour and announce exactly what broke, letting you intercept mistakes before they corrupt your results.

## Depends On

- [`dependencies`](../../repo-setup/dependencies/)
- [`project-layout`](../../repo-setup/project-layout/)

---

## The Layout

Unit tests go hand-in-hand with packages. A package gathers the reusable functions your scripts call, and those functions' behaviours are exactly what you want to pin: get them right once and every script that imports them inherits that guarantee. Here the package under test lives in `src/local_helpers/`, split into small modules:

```
src/local_helpers/
    arrays.py       # numeric array helpers
    sequences.py    # list helpers
    validation.py   # input guards
```

The tests live in `utests/`, with `test_<module>.py` per module:

```
utests/
    test_arrays.py
    test_sequences.py
    test_validation.py
```

You do not need to register each file. You point `pyproject.toml` at the folder your tests live under, and `pytest` collects every file whose name matches the pattern `test_*.py` under the path you specified:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]   # make src/ importable without installing the package
testpaths = ["utests"] # point pytest to where your test files live
```

`pytest` is itself a dependency, but only for *developing* the code, not running it, so it lives in a separate group rather than alongside the package's real dependencies. `uv` installs that group by default, so running the suite stays a single command:

```sh
uv run pytest
```

You should see every test pass.

---

## A Note on Test Dependencies

A few questions naturally surface here: why put `pytest` in its own group at all? When does that choice actually matter? Why did running the suite not need you to ask for it? Each is worth answering.

### Why a Separate Group

Two reasons, and only one is about size:

- **Hygiene.** Test tools are not part of what your code *does*. Keeping them out of the real dependencies means anyone who later installs your package as a library never has `pytest` forced on them.
- **Weight.** A development toolchain is usually far heavier than the code's runtime needs. Leaving it out gives a smaller, faster install wherever the code only has to *run*.

For a purely local lesson like this one, the hygiene point is mostly intent: there is no consumer yet to protect. The weight point only bites once the group grows, which it does quickly in real projects.

### `dev` Is Included by Default

`uv` treats the group named `dev` as its default and installs it automatically. So you never ask for the test tools; you ask to *avoid* them, with `--no-dev` for a lean, runtime-only install. (Any other group name flips this: `uv` skips it unless you opt in with `--group <name>`.) That default is why `uv run pytest` above just worked.

The split pays off at the boundaries where the code is consumed rather than developed: a built package leaves the `dev` group out of its metadata entirely, and a production or CI install drops it with `uv sync --no-dev`.

### When the Group Grows Large

A library's runtime might be a single package while its dev group balloons into whole toolchains:

- **testing:** `pytest` and its plugins (`pytest-cov`, `hypothesis`, ...)
- **lint and types:** `ruff`, `mypy`, `pre-commit`, `types-*` stubs
- **docs:** `sphinx` or `mkdocs-material`, which pull in large trees
- **notebooks:** `jupyter`, `ipython`, and their many sub-dependencies
- **fixtures and mocks:** `faker`, `responses`, `testcontainers`
- **build and release:** `build`, `twine`, `hatch`

Docs and notebook stacks are the usual reason a dev group dwarfs the runtime: hundreds of megabytes the running code never touches. That is the point where `--no-dev` stops being tidy and starts saving real time on every CI run and container build.

---

## Anatomy of a Test

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

## Different Checks for Different Abilities

Each module is paired with the kind of assertion that fits what it does. Reach for the one that matches the ability you are pinning:

- **`test_arrays.py` -> floating-point results.** Never compare floats with `==`; rounding makes that brittle. Use `numpy.testing.assert_array_almost_equal` for arrays, and `assertTrue(numpy.isnan(...))` to pin the `nan` that `safe_log10` returns for non-positive inputs.
- **`test_sequences.py` -> exact results.** Lists of integers have one right answer, so `assertEqual` compares them directly, element for element.
- **`test_validation.py` -> raised errors.** A guard's job is to *reject* bad input, so the behaviour under test is the exception itself. `with self.assertRaises(ValueError):` passes only when the call raises.

---

## Try Breaking Something

The fastest way to see what each assertion guards is to break the thing it guards:

1. Open `src/local_helpers/arrays.py` and change `normalise` to divide by `largest` instead of `largest - smallest`.
2. Run `uv run pytest`.
3. `test_maps_to_unit_range` fails, and the report shows the expected values next to the wrong ones.
4. Undo the change and watch it pass again.

Repeat with the others: drop the `raise` in `require_positive` and `test_zero_raises` fails; return the wrong slice from `chunk` and `assertEqual` flags the mismatch. The test that fails points straight at the ability you broke.

---

## Unit Tests vs Validation Tests

Unit tests are fast and deterministic: a fixed input has a single known answer. Some properties do not fit that mould, such as "does this method converge at the expected rate?", where the answer is a trend across resolutions rather than a single value. Those belong in a separate *validation* test; the convergence check in the [`finite-differences`](../../modelling-data/finite-differences/) lesson is exactly that kind of test.
