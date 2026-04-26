---
name: commit
description: This skill should be used when the user asks to "commit", "commit these changes", "commit staged files", "make a commit", "create a commit", or "write a commit message". Drafts a Conventional Commits-formatted message from staged changes and creates the commit, preferring to amend or fixup into an existing commit on unpublished branches where the changes logically belong.
context: fork
agent: general-purpose
model: opus
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Bash(git blame:*), Bash(git add:*), Bash(git reset:*), Bash(git restore:*), Bash(git commit:*), Bash(git rebase:*), Bash(git rev-parse:*), Bash(git config:*), Bash(git branch:*), AskUserQuestion
---

# commit

Create a commit for staged changes. On unpublished branches, prefer to amend or squash into the commit the changes logically belong to, rather than stacking a new commit that pollutes history.

## Decide: one commit, several commits, amend, or fixup

Before writing a message, pick one of these outcomes:

1. **New commit** — the changes introduce something independent, or the target commit is published, or it was authored by someone else.
2. **Amend HEAD** — the changes clearly belong to the immediately previous commit, that commit is unpublished, and it was authored by the current user.
3. **Fixup earlier commit** — the changes belong to an earlier unpublished commit (e.g., fixing a typo introduced three commits ago) authored by the current user.
4. **Split into multiple commits** — the staged changes cover two or more independent concerns (e.g., a refactor plus an unrelated bug fix, or a feature plus dependency bump). Each concern belongs in its own commit so history stays bisectable and reviewable.

Scan `git diff --cached` for independence signals before choosing. If the diff touches unrelated subsystems, mixes refactor with behavior change, or would require a commit message with "and" between distinct ideas, prefer splitting. When unsure, propose the split to the user via AskUserQuestion before committing as a single unit.

To choose, gather the context:

1. `git status` — see staged files
2. `git diff --cached` — examine the actual changes
3. `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null` — find the upstream, if any
4. `git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline -10` — list unpublished commits on this branch
5. For each candidate target commit, identify who authored it: `git log -1 --format='%ae %s' <sha>` and compare to `git config user.email`
6. If the staged change touches code introduced by a specific commit, use `git blame -- <file>` or `git log -p -- <file>` to locate it

When the right choice is not obvious, use the AskUserQuestion tool before acting.

## Safety rules

- **Published commits**: a commit reachable from `@{u}` is published. Default to a new commit. Only rewrite a published commit if the user explicitly asks and understands a force-push will be required.
- **Another user's commit**: if the target commit's author email differs from `git config user.email`, do not amend or fixup into it. Ask the user via AskUserQuestion what to do (new commit on top, ask them to rebase, etc.).
- **Pull requests**: apply the same logic. A PR branch whose HEAD has not been shared since the last rewrite behaves as unpublished locally — but if reviewers have commented on the commits or others have based work on it, treat it as published and ask the user before rewriting.
- **Uncommitted state**: never run a rebase while the working tree has unstaged changes unrelated to the fixup.

## Workflows

### New commit (default)

1. Run `git log --oneline -5` to match existing style
2. Draft the message (see "Message format" below)
3. Show the proposed message to the user
4. Commit using HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
type: short description

- Why this change was made
- Any non-obvious reasoning
EOF
)"
```

5. Verify with `git log -1 --stat`

### Amend HEAD

Use when the staged changes belong to the previous commit and both safety rules pass.

1. Inspect the current message: `git log -1 --format='%B'`
2. Decide whether to keep or revise the message. If reworking, draft a new one and show it to the user.
3. Amend:

```bash
# Keep existing message
git commit --amend --no-edit

# Or replace the message
git commit --amend -m "$(cat <<'EOF'
type: revised description

- Updated reasoning
EOF
)"
```

4. Verify with `git log -1 --stat`

### Split into multiple commits

Use when the staged changes cover independent concerns.

1. Group the staged changes mentally: which files or hunks belong to commit A, which to commit B, etc. Show the proposed grouping to the user before acting.
2. Unstage everything: `git reset`
3. For each group, stage only its files or hunks, then commit:

```bash
# By file
git add <files-for-group-A>
git commit -m "$(cat <<'EOF'
type: description for group A
EOF
)"

# By hunk (when groups share files)
git add -p <file>
# Select y/n per hunk, then commit as above
```

4. Verify with `git log --oneline -N` (N = number of new commits)

If a group turns out to belong to an earlier commit, fall through to the Fixup workflow for that group instead of creating a new commit.

### Fixup into an earlier commit

Use when the staged changes belong to an earlier unpublished commit authored by the current user.

1. Identify the target `<sha>` and confirm authorship and publication state
2. Create a fixup commit:

```bash
git commit --fixup=<sha>
```

3. Autosquash without opening the editor:

```bash
GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <sha>^
```

4. Verify with `git log --oneline @{u}..HEAD` (or `-10` if no upstream)

If the rebase stops on a conflict, do not force-resolve blindly — surface the conflict to the user.

## Message format

**Short line**: `type: description`
- ≤100 columns
- Clear in user-facing terms
- Common types: feat, fix, chore, docs, style, refactor, test, perf

**Body** (optional): explain *why*
- Each line wrapped at 100 columns
- Focus on goal and reasoning, not the diff
- Prose, bullets, or a mix — whatever fits the change
