# uv

One command replaces your entire environment setup. That is the trade.

---

## The script

`script.py` depends on three packages. Copy it somewhere outside this repo so you can feel the problem it solves:

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

The dependencies are declared at the top of the script:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "scipy",
# ]
# ///
```

`uv` reads this block, installs what is needed, and runs the script. One command, on any machine:

```sh
uv run script.py
```

No activate. No deactivate. No remembering what to install.

---

> **Notebook users:** launch with `uv run jupyter lab` to drop straight into the project environment. In VS Code, select the `.venv` kernel once in the kernel picker. Either way, no manual activation needed.

---

## Going further

When your work grows beyond a single script, `uv init` sets up a full project structure and `uv add` manages dependencies going forward. The [uv docs](https://docs.astral.sh/uv/) are some of the best tooling documentation written.
