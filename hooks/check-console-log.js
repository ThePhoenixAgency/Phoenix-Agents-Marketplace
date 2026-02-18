// Hook: check-console-log
// Created: 2026-02-18
// Check global console.log dans les fichiers modifies avant stop
const { execSync } = require('child_process');
module.exports = {
    run(context) {
        try {
            const result = execSync('git diff --cached --name-only 2>/dev/null || git diff --name-only', {
                timeout: 5000, stdio: 'pipe', encoding: 'utf8',
            });
            const files = result.trim().split('\n').filter(f => f.match(/\.(js|ts|jsx|tsx)$/));
            if (files.length === 0) return { status: 'ok' };
            const warnings = [];
            const fs = require('fs');
            for (const file of files) {
                try {
                    const content = fs.readFileSync(file, 'utf8');
                    if (content.includes('console.log')) warnings.push(file);
                } catch { /* skip */ }
            }
            if (warnings.length > 0) {
                return { status: 'warning', message: `[WARNING] console.log found in: ${warnings.join(', ')}` };
            }
        } catch { /* git not available */ }
        return { status: 'ok' };
    },
};
