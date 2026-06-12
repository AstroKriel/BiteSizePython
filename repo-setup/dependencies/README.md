# dependencies

One command to rule them all.

If you have not already, install `uv` by following the instructions in the [repo root README](../../README.md#getting-started).

---

## The Script

Here we will work with a `script.py` that depends on three third-party packages, showing different workflows to get it working. For now, we need not worry about which packages this script uses; in fact, when using a package manager like `uv`, that is kind of the point.

---

## The Old Way

I am sure you have been here before. You start a new project, write your first script, and now face the task of needing to work through the boilerplate steps to initialise a Python environment; this requires you to remember which packages you need, which commands to install them, you then need to activate the environment in order to run the script, and then tear it down when you are done. To remind you what this looks like, work through the following, or skip to the next section to see the simpler solution `uv` offers.

### Setup

From inside this lesson folder, make a subfolder and copy the script into it:

```sh
mkdir the-old-way
cp script.py the-old-way/
cd the-old-way
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

### Reproducibility

To make this project reproducible, capture your environment before deactivating:

```sh
pip freeze > requirements.txt
deactivate
```

This file is not created or updated automatically. You need to remember to regenerate it every time you add or remove a package.

To see reproducibility in action, delete the environment:

```sh
rm -rf .venv
```

Recreate it:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install from the requirements file:

```sh
pip install -r requirements.txt
```

Run the script:

```sh
python3 script.py
```

Deactivate when done:

```sh
deactivate
```

```
the-old-way/
├── script.py
├── requirements.txt
└── .venv/
```

---

## The uv Way

`uv` does away with most of that boilerplate. In exchange for rooting your commands in `uv` (`uv run` instead of `python`, `uv add` instead of `pip install`) your Python environment is created and managed for you.

### Setup

To see this in action, work through the same process, this time using `uv`. From inside this lesson folder, make a subfolder and copy the script into it:

```sh
mkdir the-uv-way
cp script.py the-uv-way/
cd the-uv-way
```

Initialise a uv project:

```sh
uv init .
```

Add the dependencies:

```sh
uv add numpy scipy matplotlib
```

Expected output:

```
Resolved 18 packages in 234ms
Prepared 12 packages in 1.45s
Installed 12 packages in 89ms
 + matplotlib==3.10.0
 + numpy==2.2.1
 + scipy==1.15.0
 ...
```

Notice the timings, and compare them to how long `pip install` of the same three packages took. `uv` parallelises downloads and shares a global package cache across all your `uv` projects, so it is faster than `pip` on first install and near-instant on any subsequent install of a package you already have.

Run the script:

```sh
uv run script.py
```

It works! At no point did you create, activate, or deactivate an environment. `uv` set one up in the background and `uv run` used it automatically; now anyone with `uv` can clone or copy the folder and be running immediately.

> **Tip:** if you do not know which packages a script needs (for example, when migrating an existing script to `uv`), you can skip naming them upfront. Just `uv run script.py` and `uv` will report the first missing module; `uv add` it and repeat until the script runs.

### What uv Created

After `uv init` and a few `uv add`s, your folder now contains a handful of files worth knowing about.

```
the-uv-way/
├── script.py
├── main.py
├── pyproject.toml
├── uv.lock
├── .python-version
└── .venv/
```

`pyproject.toml` declares your project's name and dependencies. `uv add` and `uv remove` keep the list of third-party dependencies up to date, so you rarely need to edit this file by hand.

`uv.lock` contains the completely resolved dependency tree: your dependencies and all of their sub-dependencies, each pinned to an exact version. `uv` negotiates all of these versions for you, finding a combination that satisfies every constraint. You can be as specific or as loose as you like with version requirements, and it will work out what is compatible. Anyone with `uv` can use this file to reproduce your exact environment.

`.python-version` pins the Python version for this project, so the same interpreter is used everywhere.

`.venv/` is the virtual environment, created and managed by `uv`. You never need to or ever should touch it directly.

> **Note:** `uv init` creates a `main.py` as a placeholder script. I suggest you delete it; we will prefer giving scripts meaningful names and placing them under a `scripts/` directory rather than putting them in the project root. The [project-layout](../project-layout/) lesson covers this.

### Reproducibility

To see this for yourself, remove the environment:

```sh
rm -rf .venv/
```

This is what a fresh start looks like: a colleague cloning your repo, or you on a new machine. The virtual environment is not committed to version control, but `pyproject.toml`, `uv.lock`, and `.python-version` are, and that is all `uv` needs. Run:

```sh
uv sync
uv run script.py
```

It works again!


## Going Further

The [uv docs](https://docs.astral.sh/uv/) provides a comprehensive overview of `uv` and the workflows it supports. It's worth a read! What we cover here is the basics, and useful core functionality, but `uv` can do a lot more.
