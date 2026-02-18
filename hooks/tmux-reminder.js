// Hook: tmux-reminder
// Created: 2026-02-18
const isInTmux = () => !!process.env.TMUX;
module.exports = {
    run(context) {
        if (!context || !context.toolInput) return { status: 'ok' };
        const command = context.toolInput.command || '';
        const longRunning = ['npm run', 'yarn', 'docker', 'make', 'cargo build'];
        const isLong = longRunning.some(cmd => command.includes(cmd));
        if (isLong && !isInTmux()) {
            return { status: 'warning', message: '[INFO] Consider running long commands in tmux.' };
        }
        return { status: 'ok' };
    },
};
