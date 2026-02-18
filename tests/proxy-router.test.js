// Tests: Proxy Router
// Created: 2026-02-18

const { ProxyRouter, DEFAULT_PROVIDERS } = require('../scripts/proxy-router');

describe('ProxyRouter', () => {
    let router;

    beforeEach(() => {
        router = new ProxyRouter({
            providers: [
                {
                    id: 'ollama',
                    name: 'Ollama',
                    type: 'local',
                    baseUrl: 'http://localhost:11434',
                    capabilities: ['basic', 'advanced'],
                    status: 'available',
                },
                {
                    id: 'lm-studio',
                    name: 'LM Studio',
                    type: 'local',
                    baseUrl: 'http://localhost:1234',
                    capabilities: ['basic', 'advanced'],
                    status: 'available',
                },
                {
                    id: 'openai',
                    name: 'OpenAI',
                    type: 'cloud',
                    baseUrl: 'https://api.openai.com',
                    capabilities: ['basic', 'advanced', 'expert'],
                    status: 'available',
                },
            ],
            defaultProvider: 'ollama',
        });
    });

    test('should route T1 requests to local providers first', () => {
        const provider = router.route({ tier: 'T1' });
        expect(provider).toBeDefined();
        expect(provider.type).toBe('local');
    });

    test('should route T2 requests to local providers first', () => {
        const provider = router.route({ tier: 'T2' });
        expect(provider).toBeDefined();
        expect(provider.type).toBe('local');
    });

    test('should route T3 requests to expert-capable providers', () => {
        const provider = router.route({ tier: 'T3' });
        expect(provider).toBeDefined();
        expect(provider.capabilities).toContain('expert');
    });

    test('should default to T1 if tier not specified', () => {
        const provider = router.route({});
        expect(provider).toBeDefined();
    });

    test('should return null if no providers available', () => {
        const emptyRouter = new ProxyRouter({ providers: [], defaultProvider: 'none' });
        const provider = emptyRouter.route({ tier: 'T1' });
        expect(provider).toBeNull();
    });

    test('should skip unavailable providers', () => {
        router.providers[0].status = 'unavailable';
        router.providers[1].status = 'unavailable';

        const provider = router.route({ tier: 'T1' });
        expect(provider).toBeDefined();
        expect(provider.id).toBe('openai');
    });

    test('should add new providers', () => {
        const initialCount = router.providers.length;
        router.addProvider({
            id: 'custom',
            name: 'Custom',
            type: 'local',
            capabilities: ['basic'],
            status: 'available',
        });
        expect(router.providers.length).toBe(initialCount + 1);
    });

    test('DEFAULT_PROVIDERS should include ollama and lm-studio', () => {
        expect(DEFAULT_PROVIDERS).toHaveLength(2);
        expect(DEFAULT_PROVIDERS.map(p => p.id)).toContain('ollama');
        expect(DEFAULT_PROVIDERS.map(p => p.id)).toContain('lm-studio');
    });
});
