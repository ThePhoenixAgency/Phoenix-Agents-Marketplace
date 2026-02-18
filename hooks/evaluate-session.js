// Hook: evaluate-session
// Created: 2026-02-18
// Evalue la session pour extraire des patterns reutilisables
module.exports = {
    run(context) {
        const patterns = [];
        if (context.errorCount && context.errorCount > 3) {
            patterns.push('High error rate - review approach');
        }
        if (context.filesModified && context.filesModified.length > 20) {
            patterns.push('Many files modified - consider splitting PRs');
        }
        if (patterns.length > 0) {
            return { status: 'ok', message: `[INFO] Session patterns: ${patterns.join('; ')}` };
        }
        return { status: 'ok' };
    },
};
