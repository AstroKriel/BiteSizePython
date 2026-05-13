# uv

One command to rule them all. (Lord of the Rings, J.R.R. Tolkien)

---

## The script

Here we will work with a `script.py` that depends on three packages. For now, we need not worry what these dependencies are. That is rather the point.

---

## The old way

You have been here before. Set up the environment, remember which packages you need, install them, run the script, tear it down.

Make a folder and copy the script into it:

```sh
mkdir -p ~/Downloads/python-deps/manual
cp script.py ~/Downloads/python-deps/manual/
cd ~/Downloads/python-deps/manual
```

Create a virtual environment:

```sh
python3 -m venv .venv
```

Activate it:

```sh
source .venv/bin/activate
```

Install the dependencies you need to remember:

```sh
pip install numpy scipy matplotlib
```

Run the script:

```sh
python3 script.py
```

Deactivate the virtual environment when done:

```sh
deactivate
```

If you use notebooks, the environment must be active before you launch:

```sh
source .venv/bin/activate
jupyter lab
```

Move to a new machine or hand the script to a colleague, and you start again from memory.

---

## The uv way

You do not need to know your dependencies upfront. Start the project and let `uv run` tell you what is missing.

Make a folder and copy the script into it:

```sh
mkdir -p ~/Downloads/python-deps/uv
cp script.py ~/Downloads/python-deps/uv/
cd ~/Downloads/python-deps/uv
```

Initialise a uv project:

```sh
uv init .
```

Try running. `uv` will tell you what is missing:

```sh
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

If you use notebooks, the environment still needs to be active before you launch. With `uv` this is one command:

```sh
uv run jupyter lab
```

In VS Code, select the `.venv` kernel once in the kernel picker and you are set.

### What uv created

| File | Purpose |
|---|---|
| `pyproject.toml` | Project name, Python version constraint, and dependencies |
| `uv.lock` | Exact versions of every package. The environment is fully reproducible. |
| `.python-version` | Pins the Python version for this project. |
| `.venv/` | The virtual environment, created and managed by `uv`. You never touch it. |


## Going further

The [uv docs](https://docs.astral.sh/uv/) are some of the best tooling documentation written. Worth a read if you want to understand the internals or the full feature set.
