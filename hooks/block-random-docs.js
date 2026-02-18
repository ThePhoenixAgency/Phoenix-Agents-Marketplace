// Hook: block-random-docs
// Created: 2026-02-18
// Bloque la creation de fichiers .md arbitraires (temp, final, todo_v2, etc.)

const ALLOWED_DOCS = [
    'README.md',
    'CHANGELOG.md',
    'INSTALL.md',
    'CONTRIBUTING.md',
    'SPONSOR.md',
    'ARCHITECTURE.md',
    'BACKLOG.md',
    'SECURITY.md',
    'SKILL.md',
];

const FORBIDDEN_PATTERNS = [
    /temp/i,
    /final/i,
    /todo_v/i,
    /draft/i,
    /notes_/i,
    /archi_/i,
    /backup/i,
];

module.exports = {
    run(context) {
        if (!context || !context.toolInput) return { status: 'ok' };

        const filePath = context.toolInput.filePath || context.toolInput.path || '';
        if (!filePath.endsWith('.md')) return { status: 'ok' };

        const fileName = filePath.split('/').pop();

        const isAllowed = ALLOWED_DOCS.includes(fileName);
        const isForbidden = FORBIDDEN_PATTERNS.some(p => p.test(fileName));

        if (isForbidden && !isAllowed) {
            return {
                status: 'blocked',
                message: `[ERROR] "${fileName}" looks like a random doc file. Use standard files (README.md, CHANGELOG.md, etc.) or place in /private/.`,
            };
        }

        return { status: 'ok' };
    },
};
