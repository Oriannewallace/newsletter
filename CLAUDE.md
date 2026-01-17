# Claude Code Rules for The Winning Formula

## GitHub Account
**Always use the `Oriannewallace` GitHub account** (not `oriwallace`) for all GitHub operations including:
- Creating repositories
- Pushing commits
- Creating pull requests
- Any other GitHub CLI operations

When using `gh` commands, ensure you're operating under the correct account.

## Security - API Keys
**NEVER commit API keys or secrets to the repository.** Before any commit:
1. Check for `.env` files - should never be committed
2. Check for `.mcp.json` - contains API keys, should never be committed
3. Check for any hardcoded API keys in code files

Files with secrets should be in `.gitignore`. Use `.example` templates for config files that need API keys.
