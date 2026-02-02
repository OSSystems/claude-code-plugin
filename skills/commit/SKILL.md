---
description: Create a conventional commit for staged changes
disable-model-invocation: true
context: fork
agent: general-purpose
model: opus
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*)
---

# Conventional Commit

Create a commit for all staged changes using conventional commit format.

## Requirements

1. **Short message**: Use conventional commit format (`type: description`)
   - Must be ≤100 columns
   - Be as clear as possible in user-facing terms
   - Common types: feat, fix, chore, docs, style, refactor, test, perf

2. **Body**: Explain why the changes were made
   - Each line wrapped at 100 columns
   - Focus on the goal and reasoning, not just what changed (the diff shows that)
   - Format flexibly: prose, bullet points, or a mix depending on context
   - Use for insightful explanations or complex concepts that need elaboration

## Steps

1. Run `git status` to see staged files
2. Run `git diff --cached` to examine actual changes
3. Run `git log --oneline -5` to check existing commit style (if any)
4. Draft a conventional commit message following the requirements above
5. Show the proposed message to the user
6. Create the commit using HEREDOC format:

```bash
git commit -m "$(cat <<'EOF'
type: short description here

- Bullet point explaining change
- Another bullet point
EOF
)"
```

7. Verify with `git log -1 --stat`
