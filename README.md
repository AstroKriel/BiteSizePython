# Bite-Size Python

Short and simple Python demos.

---

## Getting started

Most lessons require [`uv`](https://docs.astral.sh/uv/). Install it once:

**Linux**
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**macOS**
```sh
brew install uv
```

Then clone this repo and go into any lesson folder. Each one has its own `pyproject.toml`; run scripts with `uv run <script>.py` and `uv` handles the rest. See the [`dependencies` lesson](repo-setup/dependencies/) for a hands-on introduction to the tool.

---

### Building a Productive Repo

- [x] **[`uv` for dependency management](repo-setup/dependencies/):** one command to manage your project and reproduce your entire environment
- [x] **[`git` version control](repo-setup/git-basics/):** the git commands and workflows worth knowing
- [x] **[`git` branches](repo-setup/git-branches/):** isolate work in a branch, open a PR, and clean up after merging
- [x] **[Repo structure that enforces intent](repo-setup/project-layout/):** a layout that makes it easier to think clearly about your work
- [ ] **Building a reusable library:** turn a collection of scripts into something you can import, share, and depend on
- [ ] **Git submodules:** update your dev tools in one place, and every repo gets them

---

### Modelling Your Data

- [x] **[Structured data](modelling-data/structured-data/):** named fields, built-in validation, and immutability; wrap your data once and stop thinking about it
- [x] **[Finite differences](modelling-data/finite-differences/):** numerical derivatives from discrete samples; verify your method converges at the expected rate
- [x] **[Vector calculus](modelling-data/vector-calculus/):** compute field curvature with einsum; one line of index notation replaces nested for loops
- [ ] **Pipeline classes:** a few special methods and your class behaves like it was always part of the language

---

### Writing Better Functions

- [ ] **Thinking functional:** keep functions focused on one job and testing becomes trivial
- [ ] **Type validation:** stop bad inputs at the door; clear errors every time
- [x] **[Unit tests](writing-functions/unit-tests/):** catch mistakes in your pipeline before they corrupt your results
