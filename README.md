# OS Systems Claude Code Plugin

Company-wide development tools and standards for Claude Code.

## Installation

```bash
claude plugins:add OSSystems/claude-code-plugin
```

## Skills

### `/commit`

Create conventional commits for staged changes. This skill:

- Analyzes staged changes with `git diff --cached`
- Generates commit messages following [Conventional Commits](https://www.conventionalcommits.org/) format
- Writes clear, user-facing descriptions (≤100 columns)
- Includes a body explaining the reasoning behind changes

### `/refactor-claude-md`

Refactor CLAUDE.md files following progressive disclosure principles. This skill:

- Identifies contradictions in existing instructions
- Extracts only essential info for the root CLAUDE.md
- Groups remaining instructions into logical categories
- Creates a modular file structure with linked documentation
- Flags redundant or overly vague instructions for deletion

## License

MIT
