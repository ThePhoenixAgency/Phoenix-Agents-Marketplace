// Tests: Agent Registry
// Created: 2026-02-18

const { AgentRegistry } = require('../scripts/agent-registry');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('AgentRegistry', () => {
    let tmpDir;
    let registry;

    beforeEach(() => {
        tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agents-'));

        // Creer des fichiers agents de test
        fs.writeFileSync(path.join(tmpDir, 'test-agent.md'), [
            '# Test Agent',
            '# Tier: T1',
            '# Mode: on-demand',
            '',
            '## Role',
            'Agent de test.',
        ].join('\n'));

        fs.writeFileSync(path.join(tmpDir, 'security-agent.md'), [
            '# Security Agent',
            '# Tier: T3',
            '# Mode: H24',
            '',
            '## Role',
            'Securite.',
        ].join('\n'));

        registry = new AgentRegistry(tmpDir);
    });

    afterEach(() => {
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('should discover agents from directory', () => {
        registry.discover();
        const agents = registry.list();

        expect(agents).toHaveLength(2);
    });

    test('should parse agent metadata', () => {
        registry.discover();
        const agent = registry.get('test-agent');

        expect(agent).toBeDefined();
        expect(agent.id).toBe('test-agent');
        expect(agent.status).toBe('available');
    });

    test('should get agent by ID', () => {
        registry.discover();

        expect(registry.get('test-agent')).toBeDefined();
        expect(registry.get('nonexistent')).toBeUndefined();
    });

    test('should activate and deactivate agents', () => {
        registry.discover();

        registry.activate('test-agent');
        expect(registry.get('test-agent').status).toBe('active');
        expect(registry.get('test-agent').lastActive).not.toBeNull();

        registry.deactivate('test-agent');
        expect(registry.get('test-agent').status).toBe('available');
    });

    test('should return undefined when activating nonexistent agent', () => {
        registry.discover();
        const result = registry.activate('nonexistent');
        expect(result).toBeUndefined();
    });

    test('should list agents', () => {
        registry.discover();
        const all = registry.list();
        expect(all).toHaveLength(2);
        expect(all.map(a => a.id)).toContain('test-agent');
        expect(all.map(a => a.id)).toContain('security-agent');
    });
});
