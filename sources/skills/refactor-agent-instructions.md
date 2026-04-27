Refactor the project's agent instruction files to follow progressive disclosure principles.

Prioritize `AGENTS.md` when it exists. Treat `CLAUDE.md` as a legacy format that may still need to
be preserved or migrated. If both files exist, reconcile them into one coherent instruction set and
call out contradictions before editing.

## Instructions

Follow these steps:

1. **Find contradictions**: identify instructions that conflict with each other. Ask the user which
   version to keep before making a destructive choice.
2. **Identify the essentials**: extract only what belongs in the root instruction file:
   - one-sentence project description
   - package manager, if it is not the default for the project
   - non-standard build or typecheck commands
   - anything truly relevant to every single task
3. **Group the rest**: organize remaining instructions into logical categories such as TypeScript
   conventions, testing patterns, API design, or git workflow. Each category should move into its
   own markdown file.
4. **Create the file structure**: produce:
   - a minimal root instruction file with markdown links to supporting documents
   - each supporting document with only the instructions relevant to that category
   - a suggested `docs/` or similar folder structure when the repository has no existing convention
5. **Flag for deletion**: identify instructions that are redundant, too vague to be actionable, or
   overly obvious.

## Output expectations

- If the repository already uses `AGENTS.md`, keep that as the primary root file.
- If the repository only uses `CLAUDE.md`, preserve it unless the user explicitly wants a rename or
  migration plan.
- When both exist, recommend converging on a single primary file and note any compatibility concerns
  for the active harnesses.
- Prefer smaller linked documents over one long instruction file.

## Reference

The workflow is based on progressive disclosure guidance for agent instruction files.

