# Hooks
<!-- Created: 2026-02-18 | Last Updated: 2026-02-23 -->

Lifecycle hooks for automated checks and actions.

## Configuration

See `hooks.json` for the full hook configuration.

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `block-dev-outside-tmux` | PreToolUse | Block dev servers outside tmux |
| `tmux-reminder` | PreToolUse | Tmux reminder for long-running commands |
| `git-push-review` | PreToolUse | Checklist before git push |
| `block-random-docs` | PreToolUse | Block arbitrary .md files |
| `suggest-compact` | PreToolUse | Context compaction reminder |
| `pre-compact` | PreCompact | Save state |
| `session-start` | SessionStart | Package manager detection |
| `pr-log` | PostToolUse | Log PR URL |
| `post-edit-format` | PostToolUse | Auto-format with Prettier |
| `post-edit-typecheck` | PostToolUse | TypeScript check |
| `post-edit-console-warn` | PostToolUse | Warning on console.log |
| `check-console-log` | Stop | Global console.log scan |
| `session-end` | SessionEnd | Session persistence |
| `evaluate-session` | SessionEnd | Pattern extraction |
