// Hook: block-dev-outside-tmux
// Created: 2026-02-18
// Bloque les dev servers (npm run dev, etc.) lances hors d'une session tmux

const isInTmux = () => !!process.env.TMUX;

const DEV_COMMANDS = [
    'npm run dev',
    'npm start',
    'yarn dev',
    'pnpm dev',
    'npx next dev',
    'npx vite',
    'python manage.py runserver',
    'flask run',
    'go run',
];

module.exports = {
    run(context) {
        if (!context || !context.toolInput) return { status: 'ok' };

        const command = context.toolInput.command || '';
        const isDevCommand = DEV_COMMANDS.some(cmd => command.includes(cmd));

        if (isDevCommand && !isInTmux()) {
            return {
                status: 'blocked',
                message: '[WARNING] Dev server detected outside tmux. Use tmux to avoid blocking the session.',
            };
        }

        return { status: 'ok' };
    },
};
