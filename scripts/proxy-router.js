// Script: Proxy Router
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Route les requetes vers le modele LLM optimal selon le tier

/**
 * Routes LLM requests to the optimal provider based on
 * tier requirements. Prefers local (free) providers.
 */
class ProxyRouter {
    /**
     * @param {Object} config - Router configuration
     * @param {Object[]} config.providers - Available LLM providers
     * @param {string} config.defaultProvider - Fallback provider ID
     */
    constructor(config) {
        this.providers = config.providers || [];
        this.defaultProvider = config.defaultProvider || 'ollama';
    }

    /**
     * Add a new provider to the pool.
     * @param {Object} provider - Provider configuration
     */
    addProvider(provider) {
        this.providers.push(provider);
    }

    /**
     * Route a request to the best available provider.
     * Prefers local providers to minimize cost.
     * @param {Object} request - Request with tier requirement
     * @param {string} [request.tier='T1'] - Required tier (T1/T2/T3)
     * @returns {Object|null} Selected provider or null
     */
    route(request) {
        const tier = request.tier || 'T1';
        const available = this.providers.filter(p => p.status === 'available');

        const tierMap = {
            T1: (p) => p.capabilities.includes('basic'),
            T2: (p) => p.capabilities.includes('advanced'),
            T3: (p) => p.capabilities.includes('expert'),
        };

        const filter = tierMap[tier] || tierMap.T1;
        const suitable = available.filter(filter);

        if (suitable.length === 0) {
            return available[0] || null;
        }

        const local = suitable.filter(p => p.type === 'local');
        if (local.length > 0) return local[0];

        return suitable[0];
    }
}

/** Pre-configured local LLM providers. */
const DEFAULT_PROVIDERS = [
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
];

module.exports = { ProxyRouter, DEFAULT_PROVIDERS };
