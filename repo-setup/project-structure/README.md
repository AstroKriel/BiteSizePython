# project structure

A place for everything, and everything has a place.

---

## The layout

Separate what you run from what you reuse, and keep generated outputs out of the way.

```
my-project/
├── scripts/            # one script per task, runnable top-to-bottom
├── src/
│   └── local_helpers/  # shared code that scripts draw from
├── datasets/           # input data, hidden from git by default
├── figures/            # generated outputs, hidden from git by default
├── pyproject.toml      # project name, Python version, dependencies, and build backend
├── uv.lock             # pinned versions of every dependency
├── .python-version     # pins the python version for this project
└── .gitignore          # files and folders excluded from being tracked by git
```

This folder is an example of this kind of layout.

---

## .gitignore

Hide entire directories by default, then use `!` to negate specific files you want to keep. Note, `git` does not track empty directories, so `figures/` and `datasets/` will not be tracked until you store content under them.

```
## python
.venv/        # virtual environment: installed packages
__pycache__/  # stores compiled *.pyc Python bytecode

## ignore generated outputs by default
datasets/
figures/

## track outputs intentionally (! tells gitignore to not ignore)
!figures/key_result.png
```

---

## pyproject.toml

As a project grows, the same helpers tend to appear across multiple scripts. Copying them between files is fragile, so instead centralise the implementation and store shared code under `src/local_helpers/`, then import it. This kind of structure is deliberate; it forces you to build in a way that scales naturally as the project grows.

To make `src/` importable from your scripts, add a `[build-system]` block to your `pyproject.toml`:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/<package-name>"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

`[build-system]` tells `uv` how to make your local package importable. `[tool.hatch.build.targets.wheel]` tells hatchling where to find it; replace `<package-name>` with the name of your folder inside `src/`. `uv run` picks it up automatically; no extra steps needed. `hatchling` is the right default: it is what `uv` uses out of the box and requires no configuration. `setuptools` and `distutils` are older options you may encounter in the wild, but they predate modern workflows and are not worth reaching for in new projects.

---

## Import order in scripts

The official Python style guide (`PEP 8`) requires imports to be grouped in the following order: standard library first, then third-party packages, and finally local packages. This keeps dependencies visible. Within each import block, sort packages alphabetically. None of this is enforced, but it's a good rule to follow.

```python
## standard libraries
import <std-package>

from <std-package> import <module>

## third-party packages
import <third-party-package>

from <third-party-package> import <module>

## local packages
import <local-package>

from <local-package> import <module>
```

Each tier has a different origin:

- Standard library modules ship with Python, so nothing needs to be installed.
- Third-party packages are installed by `uv` from the dependencies in `pyproject.toml`; you just need to list them.
- Your local package needs to be built before it can be imported. The `[build-system]` block tells `uv` where your code lives; by convention this is `src/<package-name>`. As you add code there, `uv` handles the rest.
