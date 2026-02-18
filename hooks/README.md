# Hooks
<!-- Created: 2026-02-18 | Last Updated: 2026-02-18 -->

Lifecycle hooks for automated checks and actions.

## Configuration

See `hooks.json` for the full hook configuration.

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `block-dev-outside-tmux` | PreToolUse | Bloque dev servers hors tmux |
| `tmux-reminder` | PreToolUse | Rappel tmux pour commandes longues |
| `git-push-review` | PreToolUse | Checklist avant git push |
| `block-random-docs` | PreToolUse | Bloque fichiers .md arbitraires |
| `suggest-compact` | PreToolUse | Rappel compaction contexte |
| `pre-compact` | PreCompact | Sauvegarde etat |
| `session-start` | SessionStart | Detection package manager |
| `pr-log` | PostToolUse | Log URL PR |
| `post-edit-format` | PostToolUse | Auto-format Prettier |
| `post-edit-typecheck` | PostToolUse | TypeScript check |
| `post-edit-console-warn` | PostToolUse | Warning console.log |
| `check-console-log` | Stop | Scan global console.log |
| `session-end` | SessionEnd | Persistance session |
| `evaluate-session` | SessionEnd | Extraction patterns |
