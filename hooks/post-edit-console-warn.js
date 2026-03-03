// Hook: post-edit-console-warn
// Created: 2026-02-18
// Warning if console.log added in an edited file
const fs = require('fs');
module.exports = {
    run(context) {
        if (!context || !context.toolInput) return { status: 'ok' };
        const filePath = context.toolInput.filePath || context.toolInput.path || '';
        if (!filePath.match(/\.(js|ts|jsx|tsx)$/)) return { status: 'ok' };
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const lines = content.split('\n');
            const consoleLines = lines.reduce((acc, line, i) => {
                if (line.includes('console.log') && !line.trim().startsWith('//')) acc.push(i + 1);
                return acc;
            }, []);
            if (consoleLines.length > 0) {
                return { status: 'warning', message: `[WARNING] console.log found at lines: ${consoleLines.join(', ')}` };
            }
        } catch { /* file not readable */ }
        return { status: 'ok' };
    },
};
