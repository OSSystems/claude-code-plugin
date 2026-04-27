Create a commit for staged changes. On unpublished branches, prefer to amend or squash into the
commit the changes logically belong to instead of stacking a new commit that pollutes history.

## Decide: one commit, several commits, amend, or fixup

Before writing a message, pick one of these outcomes:

1. **New commit**: the changes introduce something independent, the target commit is published, or
   it was authored by someone else.
2. **Amend HEAD**: the changes clearly belong to the immediately previous commit, that commit is
   unpublished, and it was authored by the current user.
3. **Fixup earlier commit**: the changes belong to an earlier unpublished commit authored by the
   current user.
4. **Split into multiple commits**: the staged changes cover independent concerns and should remain
   bisectable.

Scan `git diff --cached` for independence signals before choosing. If the diff touches unrelated
subsystems, mixes refactor with behavior change, or would require a message with "and" between
distinct ideas, prefer splitting. When the right choice is not obvious, ask the user before acting
using the current harness's question mechanism.

Gather this context before deciding:

1. `git status`
2. `git diff --cached`
3. `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null`
4. `git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline -10`
5. `git log -1 --format='%ae %s' <sha>` for candidate target commits, compared with
   `git config user.email`
6. `git blame -- <file>` or `git log -p -- <file>` when ownership of a touched line matters

## Safety rules

- **Published commits**: if a commit is reachable from `@{u}`, treat it as published. Default to a
  new commit unless the user explicitly wants history rewritten.
- **Another user's commit**: do not amend or fix up into a commit authored by someone else.
- **Pull requests**: if the branch has already been reviewed or shared, treat it as published.
- **Uncommitted state**: do not start a rebase while unrelated unstaged changes are present.

## Workflows

### New commit

1. Run `git log --oneline -5` to match local style.
2. Draft the message using the format below.
3. Show the proposed message to the user when the harness expects confirmation.
4. Commit using a multi-line message if a body is useful.
5. Verify with `git log -1 --stat`.

### Amend HEAD

1. Inspect the current message with `git log -1 --format='%B'`.
2. Decide whether to keep or revise the message.
3. Run `git commit --amend --no-edit` or replace the message.
4. Verify with `git log -1 --stat`.

### Split into multiple commits

1. Group the staged changes into independent commits.
2. Show the grouping to the user before acting when the split is not obvious.
3. Unstage everything, then stage and commit each group separately.
4. Verify with `git log --oneline -N`.

### Fixup into an earlier commit

1. Identify the target commit and confirm authorship and publication state.
2. Create a fixup commit with `git commit --fixup=<sha>`.
3. Autosquash with `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <sha>^`.
4. Verify with `git log --oneline @{u}..HEAD` or `git log --oneline -10`.

If a rebase stops on a conflict, stop and surface the conflict instead of forcing a resolution.

## Message format

**Short line**: `type: description`

- Keep it under 100 columns.
- Use clear user-facing wording.
- Common types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `perf`.

**Body**: explain why

- Wrap lines at 100 columns.
- Focus on rationale rather than diff narration.
- Use prose, bullets, or a mix.

