# uv

One command to rule them all.

---

## The script

Here we will work with a `script.py` that depends on three packages. For now, we need not worry what these dependencies are. That is rather the point.

---

## The old way

You have been here before. Set up the environment, remember which packages you need, install them, run the script, tear it down.

Make a folder and copy the script into it:

```sh
mkdir manual
cp script.py manual/
cd manual
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
mkdir uv
cp script.py uv/
cd uv
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

If you use notebooks, start your session the same way:

```sh
uv run jupyter lab
```

This drops you straight into the project environment. No need to manually activate your environment and then launch your server.

### What uv created

`pyproject.toml` declares your project's name and dependencies. `uv add` and `uv remove` keep the list of third-party dependencies up to date, so you rarely need to edit this file by hand.

`uv.lock` contains the completely resolved dependency tree: your dependencies and all of their sub-dependencies, each pinned to an exact version. `uv` negotiates all of these versions for you, finding a combination that satisfies every constraint. You can be as specific or as loose as you like with version requirements, and it will work out what is compatible. Anyone with `uv` can use this file to reproduce your exact environment.

`.python-version` pins the Python version for this project, so the same interpreter is used everywhere.

`.venv/` is the virtual environment, created and managed by `uv`. You never need to or ever should touch it directly.


## Going further

The [uv docs](https://docs.astral.sh/uv/) provides a comprehensive overview of `uv` and the workflows it supports. It's worth a read! What we cover here is the basics, and useful core functionality, but `uv` can do a lot more.
