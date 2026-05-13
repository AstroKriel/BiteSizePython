# uv

One command to rule them all. (Lord of the Rings, J.R.R. Tolkien)

---

## The script

Here we will work with a `script.py` that depends on three packages. For now, we need not worry what these dependencies are. That is rather the point.

---

## The old way

You have been here before. Set up the environment, remember which packages you need, install them, run the script, tear it down.

```sh
mkdir -p ~/Downloads/python-deps/manual
cp script.py ~/Downloads/python-deps/manual/
cd ~/Downloads/python-deps/manual

python3 -m venv .venv
source .venv/bin/activate
pip install numpy scipy matplotlib
python3 script.py
deactivate
```

Move to a new machine or hand the script to a colleague, and you start again from memory.

---

## The uv way

You do not need to know your dependencies upfront. Start the project and let `uv run` tell you what is missing.

```sh
mkdir -p ~/Downloads/python-deps/uv
cp script.py ~/Downloads/python-deps/uv/
cd ~/Downloads/python-deps/uv

uv init .
uv run script.py
# ModuleNotFoundError: No module named 'numpy'
```

Add the missing package and try again:

```sh
uv add numpy
uv run script.py
# ModuleNotFoundError: No module named 'scipy'
```

Repeat until it runs:

```sh
uv add scipy
uv run script.py
# ModuleNotFoundError: No module named 'matplotlib'

uv add matplotlib
uv run script.py
# it works
```

No activate. No deactivate. No auditing your imports before you start. `uv` builds up the dependency list for you as you go, and once it runs, anyone with `uv` can clone or copy the folder and be running immediately.

### What uv created

| File | Purpose |
|---|---|
| `pyproject.toml` | Project name, Python version constraint, and dependencies |
| `uv.lock` | Exact versions of every package. The environment is fully reproducible. |
| `.python-version` | Pins the Python version for this project. |
| `.venv/` | The virtual environment, created and managed by `uv`. You never touch it. |

---

> **Notebook users:** launch with `uv run jupyter lab` to drop straight into the project environment. In VS Code, select the `.venv` kernel once in the kernel picker. Either way, no manual activation needed.

---

## Going further

The [uv docs](https://docs.astral.sh/uv/) are some of the best tooling documentation written. Worth a read if you want to understand the internals or the full feature set.
