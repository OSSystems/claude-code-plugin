# OS Systems Claude Code Plugins

Company-wide development tools and standards for Claude Code.

## Marketplace

Add the marketplace and install all plugins:
```
/plugin marketplace add OSSystems/claude-code-plugin
```

Or browse individual plugins below.

## Plugins

### ossystems-commit

Create conventional commits for staged changes.

**Installation:**
```
/plugin install ossystems-commit@ossystems
```

**Skill:** `/commit`
- Analyzes staged changes with `git diff --cached`
- Generates commit messages following [Conventional Commits](https://www.conventionalcommits.org/) format
- Writes clear, user-facing descriptions (≤100 columns)
- Includes a body explaining the reasoning behind changes

### ossystems-refactor-claude-md

Refactor CLAUDE.md files following progressive disclosure principles.

**Installation:**
```
/plugin install ossystems-refactor-claude-md@ossystems
```

**Skill:** `/refactor-claude-md`
- Identifies contradictions in existing instructions
- Extracts only essential info for the root CLAUDE.md
- Groups remaining instructions into logical categories
- Creates a modular file structure with linked documentation
- Flags redundant or overly vague instructions for deletion

## License

MIT
