// Hook: post-edit-format
// Created: 2026-02-18
// Auto-format avec Prettier apres chaque edit de fichier

const { execSync } = require('child_process');
const path = require('path');

const SUPPORTED_EXTENSIONS = ['.js', '.jsx', '.ts', '.tsx', '.css', '.json', '.md', '.html'];

module.exports = {
    run(context) {
        if (!context || !context.toolInput) return { status: 'ok' };

        const filePath = context.toolInput.filePath || context.toolInput.path || '';
        const ext = path.extname(filePath);

        if (!SUPPORTED_EXTENSIONS.includes(ext)) return { status: 'ok' };

        try {
            execSync(`npx prettier --write "${filePath}"`, {
                timeout: 10000,
                stdio: 'pipe',
            });
            return { status: 'ok', message: `Formatted: ${path.basename(filePath)}` };
        } catch {
            // Prettier not available or failed, skip silently
            return { status: 'ok' };
        }
    },
};
