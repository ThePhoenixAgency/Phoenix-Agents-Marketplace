# Contributing
<!-- Created: 2026-02-18 | Last Updated: 2026-02-18 -->

## Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Write tests first (TDD)
4. Implement the feature
5. Run `bash commands/workflow/validate.sh`
6. Commit with conventional format: `feat(scope): description`
7. Push and create a Pull Request

## Commit Format

```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Gemini
```

### Types
- `feat` - New feature (MINOR)
- `fix` - Bug fix (PATCH)
- `docs` - Documentation only
- `style` - Code style (no logic change)
- `refactor` - Refactoring
- `perf` - Performance improvement
- `test` - Tests
- `chore` - Maintenance
- `security` - Security fix

## Rules

- No placeholders or TODOs
- Tests must pass with >90% coverage
- JSDoc on all public functions
- No sensitive data in docs/ (use private/)
- No direct push to main

## Structure

- Agents go in `agents/`
- Skills go in `skills/<name>/SKILL.md`
- Commands go in `commands/<category>/<name>.sh`
- Hooks go in `hooks/<name>.js`
- Core scripts go in `scripts/<name>.js`
- Tests go in `tests/<name>.test.js`
