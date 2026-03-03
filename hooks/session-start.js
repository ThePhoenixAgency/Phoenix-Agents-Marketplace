// Hook: session-start
// Created: 2026-02-18
// Loads previous context, detects package manager, initializes session

const fs = require('fs');
const path = require('path');

function detectPackageManager(dir) {
    if (fs.existsSync(path.join(dir, 'bun.lockb'))) return 'bun';
    if (fs.existsSync(path.join(dir, 'pnpm-lock.yaml'))) return 'pnpm';
    if (fs.existsSync(path.join(dir, 'yarn.lock'))) return 'yarn';
    if (fs.existsSync(path.join(dir, 'package-lock.json'))) return 'npm';
    if (fs.existsSync(path.join(dir, 'Gemfile.lock'))) return 'bundler';
    if (fs.existsSync(path.join(dir, 'poetry.lock'))) return 'poetry';
    if (fs.existsSync(path.join(dir, 'go.sum'))) return 'go';
    if (fs.existsSync(path.join(dir, 'Cargo.lock'))) return 'cargo';
    return null;
}

module.exports = {
    run(context) {
        const projectDir = context.projectDir || process.cwd();
        const packageManager = detectPackageManager(projectDir);

        return {
            status: 'ok',
            data: {
                packageManager,
                sessionStartTime: new Date().toISOString(),
                projectDir,
            },
        };
    },
};
