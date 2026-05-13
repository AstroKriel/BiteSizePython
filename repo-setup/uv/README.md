# uv

One command to rule them all. (Lord of the Rings, J.R.R. Tolkien)

---

## The script

`script.py` depends on three packages. Copy it somewhere outside this repo to feel the problem it solves:

```sh
mkdir ~/Downloads/uv-demo
cp script.py ~/Downloads/uv-demo/
cd ~/Downloads/uv-demo
```

---

## The old way

Track your dependencies yourself. Remember which ones you need, install them, activate the environment, run the script, deactivate.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install numpy scipy matplotlib
python3 script.py
deactivate
```

Move to a new machine or hand the script to a colleague and you start again from memory.

---

## The uv way

Initialise a project and declare your dependencies once:

```sh
uv init .
uv add numpy scipy matplotlib
```

Then run:

```sh
uv run script.py
```

No activate. No deactivate. No remembering what to install. Anyone with `uv` can clone or copy the folder and `uv run` works immediately.

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
