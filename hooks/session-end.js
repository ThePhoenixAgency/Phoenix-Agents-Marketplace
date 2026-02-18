// Hook: session-end
// Created: 2026-02-18
// Persiste l'etat de session pour reprise
const fs = require('fs');
const path = require('path');
module.exports = {
    run(context) {
        const stateDir = path.join(process.cwd(), '.agent', 'state');
        try {
            if (!fs.existsSync(stateDir)) fs.mkdirSync(stateDir, { recursive: true });
            const state = {
                timestamp: new Date().toISOString(),
                filesModified: context.filesModified || [],
                currentTask: context.currentTask || '',
                sessionDuration: context.sessionDuration || 0,
            };
            fs.writeFileSync(path.join(stateDir, 'last-session.json'), JSON.stringify(state, null, 2));
        } catch { /* silent fail */ }
        return { status: 'ok' };
    },
};
