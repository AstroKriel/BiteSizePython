# git branches

Keep your worklow on the `main` branch clean and runnable, and isolate large feature changes in a branch that can be integrated once they are ready.

## Depends On

- [`git-basics`](../git-basics/)

---

## Why Branches

`main` is your source of truth. Work that is not finished does not belong there. A branch lets you commit freely without touching `main`, and keeps it clean enough to review and merge one change at a time.

---

## Naming

`verb/short-description`. Lowercase and hyphenated:

```
add/user-auth
fix/login-timeout
update/readme
refactor/data-loader
```

Use the same verbs as your commit messages: `add`, `fix`, `update`, `refactor`, `docs`, `del`.

On a shared repo with multiple contributors, prepend your username so branches are easy to attribute at a glance:

```
username/verb/short-description
```

| Rule | |
|---|---|
| Separators | `/` for namespaces, `-` for words within a namespace |
| Length | max 50 characters |
| Characters | alphanumeric, `-`, and `/` only |
| Avoid | dates, vague names (`wip`, `temp`, `fix-stuff`) |

---

## Creating a Branch

Always branch from the latest `origin/main`, not wherever your local checkout happens to be.

Start from the latest `origin/main`:

```sh
git fetch --prune origin
git switch -c add/feature --no-track origin/main
git push -u origin HEAD
```

`fetch --prune` refreshes remote refs and clears stale tracking refs for branches that no longer exist on the remote. `switch -c` creates and checks out the new branch. `--no-track` means it will not track `origin/main`; it will track its own remote counterpart once pushed. `push -u origin HEAD` publishes the branch and sets that upstream.

`git_helpers` does the same in one step:

```sh
git_helpers create-branch-from-default add/feature
```

---

## Working on the Branch

Same commit discipline as on `main`. One logical change per commit, clear message.

Push regularly:

```sh
git_helpers push
```

---

## If main Moves While You Are Working

Do not rebase; merge instead. Rebase rewrites commits, which causes problems if anyone else has already pulled your branch.

If commits land on `main` after you branched, your branch starts to diverge. Merge them in:

```sh
git fetch --prune origin
git merge --ff origin/main
```

`--ff` fast-forwards when histories are linear (no merge commit), and falls back to a real merge commit if they have diverged.

`git_helpers` wraps this as:

```sh
git_helpers sync-branch
```

---

## Opening a Pull Request

When the branch is ready, go to GitHub. If you pushed recently, it will show a banner prompting you to open a PR. Otherwise, navigate to the branch and click "Compare & pull request".

The PR is where changes get reviewed before landing on `main`. Keep the title in the same format as your commit messages.

---

## After the Merge

The branch has done its job. Leave stale branches around and they become clutter.

Once the PR merges, `origin/add/feature` is deleted. The local branch is now stale. Check which branches are already merged, then delete by name:

```sh
git fetch --prune origin
git branch --merged origin/main
git branch -d -- add/feature
```

`fetch --prune` clears the remote tracking ref. `branch --merged` lists local branches whose commits are already in `origin/main`. `branch -d` deletes safely; it refuses if there are unmerged commits.

`git_helpers` handles both passes in one step:

```sh
git_helpers cleanup-local-branches
```
