---
name: ci-cd-pipelines
description: GitHub Actions, GitLab CI, matrix builds, cache
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# CI/CD Pipelines
## GitHub Actions
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
```
## GitLab CI
```yaml
stages:
  - test
  - build
  - deploy
test:
  stage: test
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  script:
    - npm ci
    - npm run lint
    - npm test -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
```
## Checklist
- [ ] Tests automatises sur chaque PR
- [ ] Lint obligatoire
- [ ] Security scan (npm audit, Snyk)
- [ ] Build verification
- [ ] Coverage reporting
- [ ] Cache des dependances
- [ ] Matrix builds (multi-versions)
