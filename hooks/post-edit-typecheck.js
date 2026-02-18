// Hook: post-edit-typecheck
// Created: 2026-02-18
// TypeScript check apres edit .ts/.tsx
const { execSync } = require('child_process');
const path = require('path');
module.exports = {
    run(context) {
        if (!context || !context.toolInput) return { status: 'ok' };
        const filePath = context.toolInput.filePath || context.toolInput.path || '';
        const ext = path.extname(filePath);
        if (ext !== '.ts' && ext !== '.tsx') return { status: 'ok' };
        try {
            execSync('npx tsc --noEmit --pretty 2>&1 | head -20', { timeout: 15000, stdio: 'pipe' });
            return { status: 'ok' };
        } catch (e) {
            return { status: 'warning', message: `[WARNING] TypeScript errors detected in ${path.basename(filePath)}` };
        }
    },
};
