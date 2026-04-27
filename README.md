# OS Systems Agent Plugins

Company-wide development tools and standards for Claude Code, Codex, and future agent harnesses.

This repository now keeps plugin behavior in shared source files and generates harness-specific
artifacts for each supported runtime.

## Layout

- `sources/plugins/`: canonical plugin metadata
- `sources/skills/`: canonical skill instructions
- `plugins/*/.claude-plugin/`: generated Claude manifests
- `plugins/*/.codex-plugin/`: generated Codex manifests
- `.claude-plugin/marketplace.json`: generated Claude marketplace
- `.agents/plugins/marketplace.json`: generated Codex marketplace

## Generate Artifacts

```bash
make generate-plugins
```

## Validate Artifacts

```bash
make validate-plugins
```

## Claude Code

Add the marketplace:

```bash
/plugin marketplace add OSSystems/ai-plugins
```

Install individual plugins directly:

```bash
/plugin install ossystems-commit@ossystems
/plugin install ossystems-refactor-agent-instructions@ossystems
```

These Claude Code commands are still valid. Anthropic's current plugin documentation and plugin
announcement still describe the `/plugin marketplace add` and `/plugin install` flow.

## Codex

Add the marketplace from the command line:

```bash
codex plugin marketplace add OSSystems/ai-plugins
```

The current local Codex CLI also accepts a local checkout as the marketplace source:

```bash
codex plugin marketplace add /absolute/path/to/ai-plugins
```

The generated Codex marketplace file lives at:

```text
.agents/plugins/marketplace.json
```

After adding the marketplace, install plugins from inside the Codex CLI interactive `/plugin`
flow. The current Codex CLI on this machine exposes `codex plugin marketplace add`, but it does not
expose a standalone non-interactive `codex plugin install` subcommand.

Available Codex plugins:

- `ossystems-commit`
- `ossystems-refactor-agent-instructions`

## Plugins

### ossystems-commit

Creates conventional commits for staged changes.

### ossystems-refactor-agent-instructions

Refactors agent instruction files such as `AGENTS.md` and legacy `CLAUDE.md` using progressive
disclosure.

## License

MIT
