// Hook: pr-log
// Created: 2026-02-18
// Log l'URL de la PR apres creation via gh cli
module.exports = {
    run(context) {
        if (!context || !context.toolOutput) return { status: 'ok' };
        const output = context.toolOutput || '';
        const prUrlMatch = output.match(/https:\/\/github\.com\/[^\s]+\/pull\/\d+/);
        if (prUrlMatch) {
            return { status: 'ok', message: `[INFO] PR created: ${prUrlMatch[0]}` };
        }
        return { status: 'ok' };
    },
};
