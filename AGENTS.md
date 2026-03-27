# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Project Context: Shopping List App

A shopping list application that compares prices across Coles, Woolworths, and Aldi (Australia).

### Supermarket API Status
- **Coles**: Uses Next.js data endpoints. Requires a dynamic `buildId` extracted from the homepage.
- **Woolworths**: Uses a POST-based internal REST API. Requires a `WOL-StoreId` cookie for localized pricing (Default: `1265` for Sydney CBD).
- **Aldi**: No public search API. Strategy is user-entered prices (see ALDI.md).

### CLI Tools
- `./coles.py <query>`: Search Coles.
- `./woolworths.py <query>`: Search Woolworths.
- `./aldi.py <query>`: Search Aldi (Limited - Special Buys/Super Savers).
- `./compare.py <query>`: Compare all three supermarkets and rank by price per unit.

### API Scripts (experimental - require API keys)
- `./coles_api.py <query>`: Uses Coles official API (requires `Ocp-Apim-Subscription-Key`).
- `./woolworths_api.py <query>`: Uses Woolworths mobile API (requires `X-Api-Key`).

### Web Application
- `shopping-web/`: React web app for price comparison
  - Start: `cd shopping-web && npm start`
  - Backend: `node server.js` (runs Python scripts)

### Mobile Application
- `ShoppingApp/`: React Native mobile app (experimental)
- Status: Has issues with Metro bundler on some setups

## Context Preservation

Any changes you make, you should make sure to update README.md to reflect the current state of the project. This is critical for maintaining context for future sessions and other agents.

You should also update AGENTS.md with any new tools, commands, or workflows you establish during your work. This ensures that all agents have access to the latest information and can operate effectively.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work atomically
bd close <id>         # Complete work
bd dolt push          # Push beads data to remote
```

## Non-Interactive Shell Commands

**ALWAYS use non-interactive flags** with file operations to avoid hanging on confirmation prompts.

Shell commands like `cp`, `mv`, and `rm` may be aliased to include `-i` (interactive) mode on some systems, causing the agent to hang indefinitely waiting for y/n input.

**Use these forms instead:**
```bash
# Force overwrite without prompting
cp -f source dest           # NOT: cp source dest
mv -f source dest           # NOT: mv source dest
rm -f file                  # NOT: rm file

# For recursive operations
rm -rf directory            # NOT: rm -r directory
cp -rf source dest          # NOT: cp -r source dest
```

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
