// Hook: git-push-review
// Created: 2026-02-18
// Rappelle de reviewer les changements avant git push

module.exports = {
    run(context) {
        if (!context || !context.toolInput) return { status: 'ok' };

        const command = context.toolInput.command || '';

        if (command.includes('git push')) {
            return {
                status: 'warning',
                message: [
                    '[WARNING] About to push. Checklist:',
                    '- [ ] Tests passent (npm test)',
                    '- [ ] Lint OK (npm run lint)',
                    '- [ ] Pas de console.log',
                    '- [ ] Pas de secrets dans le diff',
                    '- [ ] Commit message conventionnel',
                    '- [ ] Co-Authored-By: Gemini',
                ].join('\n'),
            };
        }

        return { status: 'ok' };
    },
};
