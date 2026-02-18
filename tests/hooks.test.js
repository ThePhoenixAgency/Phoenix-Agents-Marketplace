// Tests: Hooks
// Created: 2026-02-18

const blockDevOutsideTmux = require('../hooks/block-dev-outside-tmux');
const gitPushReview = require('../hooks/git-push-review');
const blockRandomDocs = require('../hooks/block-random-docs');
const sessionStart = require('../hooks/session-start');

describe('block-dev-outside-tmux', () => {
    const originalTmux = process.env.TMUX;

    afterEach(() => {
        if (originalTmux) {
            process.env.TMUX = originalTmux;
        } else {
            delete process.env.TMUX;
        }
    });

    test('should return ok for non-dev commands', () => {
        delete process.env.TMUX;
        const result = blockDevOutsideTmux.run({
            toolInput: { command: 'git status' },
        });
        expect(result.status).toBe('ok');
    });

    test('should block npm run dev outside tmux', () => {
        delete process.env.TMUX;
        const result = blockDevOutsideTmux.run({
            toolInput: { command: 'npm run dev' },
        });
        expect(result.status).toBe('blocked');
    });

    test('should allow npm run dev inside tmux', () => {
        process.env.TMUX = '/tmp/tmux-1000/default,12345,0';
        const result = blockDevOutsideTmux.run({
            toolInput: { command: 'npm run dev' },
        });
        expect(result.status).toBe('ok');
    });

    test('should return ok for null context', () => {
        const result = blockDevOutsideTmux.run(null);
        expect(result.status).toBe('ok');
    });
});

describe('git-push-review', () => {
    test('should warn on git push', () => {
        const result = gitPushReview.run({
            toolInput: { command: 'git push origin main' },
        });
        expect(result.status).toBe('warning');
        expect(result.message).toContain('Checklist');
        expect(result.message).toContain('Co-Authored-By');
    });

    test('should return ok for non-push commands', () => {
        const result = gitPushReview.run({
            toolInput: { command: 'git commit -m "test"' },
        });
        expect(result.status).toBe('ok');
    });

    test('should return ok for null context', () => {
        const result = gitPushReview.run(null);
        expect(result.status).toBe('ok');
    });
});

describe('block-random-docs', () => {
    test('should block temp_notes.md', () => {
        const result = blockRandomDocs.run({
            toolInput: { filePath: '/project/docs/temp_notes.md' },
        });
        expect(result.status).toBe('blocked');
    });

    test('should block archi_final.md', () => {
        const result = blockRandomDocs.run({
            toolInput: { filePath: '/project/archi_final.md' },
        });
        expect(result.status).toBe('blocked');
    });

    test('should allow README.md', () => {
        const result = blockRandomDocs.run({
            toolInput: { filePath: '/project/README.md' },
        });
        expect(result.status).toBe('ok');
    });

    test('should allow SKILL.md', () => {
        const result = blockRandomDocs.run({
            toolInput: { filePath: '/project/skills/tdd/SKILL.md' },
        });
        expect(result.status).toBe('ok');
    });

    test('should allow non-md files', () => {
        const result = blockRandomDocs.run({
            toolInput: { filePath: '/project/src/temp.js' },
        });
        expect(result.status).toBe('ok');
    });

    test('should return ok for null context', () => {
        const result = blockRandomDocs.run(null);
        expect(result.status).toBe('ok');
    });
});

describe('session-start', () => {
    test('should detect package manager', () => {
        const result = sessionStart.run({
            projectDir: process.cwd(),
        });
        expect(result.status).toBe('ok');
        expect(result.data).toBeDefined();
        expect(result.data.sessionStartTime).toBeDefined();
        expect(result.data.projectDir).toBeDefined();
    });
});
