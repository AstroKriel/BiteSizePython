# uv

The trade: type `uv run script.py` instead of `python3 script.py`. That is the entire cost.

---

## What you are trading away

The old setup, repeated on every machine and for every new colleague:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install numpy
python3 before.py
deactivate
```

And when you move to a new machine or an HPC cluster, you start again from memory.

---

## What you get

Declare your dependencies once, alongside your code. `uv` creates the environment, installs the right versions, and runs your script on any machine with one command.

- No activate, no deactivate
- No "which packages did I need again?"
- Clone the repo on a new machine and `uv run` works immediately

> **Notebook users:** launch with `uv run jupyter lab` to drop straight into the project environment. In VS Code, select the `.venv` kernel once in the kernel picker. Either way, no manual activation needed.

---

## For a standalone script

Add a metadata block at the top. `uv` reads it and handles everything:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
# ]
# ///
```

Then: `uv run after.py`

See `before.py` and `after.py` for this in action.

---

## For a project

When your work grows beyond a single script, `uv init` sets up the structure and `uv add` manages your dependencies going forward:

```sh
uv init my-project
cd my-project
uv add numpy pandas
uv run analysis.py
```

### The files

| File | Purpose |
|---|---|
| `pyproject.toml` | Project name, Python version constraint, and dependencies |
| `uv.lock` | Exact versions of every package. The environment is fully reproducible. |
| `.python-version` | Pins the Python version (optional; can also live in `pyproject.toml`) |
| `.venv/` | The virtual environment, created and managed by `uv`. You never touch it. |

---

## Adopting on an existing project

If you already have a project, two commands are enough:

```sh
uv init .
uv add -r requirements.txt  # if you have one
```

From that point on, `uv run` works.

---

The [uv docs](https://docs.astral.sh/uv/) are some of the best tooling documentation written. Worth a read if you want to understand the internals or the full feature set.
