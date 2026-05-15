# git

A commit's a decision. Make it easy to understand six months from now.

---

## Starting a repo

```sh
git init -b main
```

This creates a repo with `main` as the default branch. Without `-b main`, `git` may default to another branch name.

---

## git_helpers

[`git_helpers`](https://github.com/AstroKriel/GitHelpers) packages common `git` workflows into useful commands that narrate the process, so you learn the ropes while getting work done. Reach for it when you are unsure, or worried about making a mistake, like syncing branches, pruning stale locals, and managing submodules. As you grow more comfortable, start taking the training wheels off.

---

## What to commit

A commit should capture one logical change: something you can describe in a single line and revert without breaking anything else.

The easy habit's to treat `git` like a save button:

```sh
git add .
git commit -m "update"
```

A history of "update" commits tells you nothing. When something breaks, you have no map.

Before staging, ask what changed. If the answer needs "and", split it into two commits. Stage specific files, not everything:

```sh
git status                # see what's in play
git add path/to/file.py   # stage what belongs in this commit
git commit -m "..."       # commit
```

---

## Writing the message

```
action(scope): details.
```

`action` describes the kind of change:

| Action | When |
|---|---|
| `add` | new functionality |
| `fix` | bug fix |
| `update` | changes to existing functionality |
| `refactor` | restructuring without behaviour change |
| `docs` | documentation only |
| `del` | deleting code or files |

`scope` describes where. Match the granularity to the change: a function name for a localised fix, a filename for a broad change in one file, a concept name for changes spread across many files.

`details` is what specifically changed: lowercase, specific, ending with a period.

```
add(analyse.py): fit a linear model and plot residuals.
fix(DataSeries): raise ValueError when array lengths differ.
docs(README.md): add setup instructions and usage examples.
refactor(main): extract plot logic into a standalone function.
```

---

## Pushing

First, connect your local repo to a remote (e.g., GitHub):

```sh
git remote add origin <url>
```

Then push and set the upstream in one step:

```sh
git push -u origin main
```

After the upstream is set, subsequent pushes are just:

```sh
git push
```

`git_helpers push` handles the upstream check automatically, using `-u` on the first push and a plain push after:

```sh
git_helpers push
```

---

## Reviewing

Check your history at any time:

```sh
git log --oneline --decorate -n 20
```

If you can read it and understand what happened and why, you are doing it right. `git_helpers` wraps this as:

```sh
git_helpers show-recent-commits
```

---

## Where this goes

This is the base of `git`. For a solo project, it's pretty much all you need.

There is more to `git`, though, and it's the part that gets a reputation for being scary. It's not. As projects grow, more developers, more moving parts, changes landing at the same time, `git` becomes the thing that keeps it all manageable. Branches let you keep work isolated until it's ready, conflicts get resolved cleanly, and history stays readable. That's where `git_helpers` will really earn its keep.
