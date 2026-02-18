// Script: Agent Registry
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Registre central des agents disponibles et leur etat

const fs = require('fs');
const path = require('path');

/**
 * Registry for discovering and managing agents.
 * Scans a directory for .md agent definition files.
 */
class AgentRegistry {
    /**
     * @param {string} agentsDir - Path to directory containing agent .md files
     */
    constructor(agentsDir) {
        this.agentsDir = agentsDir;
        /** @type {Map<string, Object>} */
        this.agents = new Map();
    }

    /**
     * Discover agents from the agents directory.
     * @returns {AgentRegistry} this (for chaining)
     */
    discover() {
        const files = fs.readdirSync(this.agentsDir).filter(f => f.endsWith('.md'));
        for (const file of files) {
            const agentId = file.replace('.md', '');
            const content = fs.readFileSync(path.join(this.agentsDir, file), 'utf8');
            const metadata = this.parseMetadata(content);
            this.agents.set(agentId, {
                id: agentId,
                file,
                ...metadata,
                status: 'available',
                lastActive: null,
            });
        }
        return this;
    }

    /**
     * Parse metadata from agent markdown content.
     * @param {string} content - Markdown content
     * @returns {Object} Extracted metadata
     */
    parseMetadata(content) {
        const lines = content.split('\n');
        const metadata = {};
        for (const line of lines) {
            if (line.startsWith('# ')) metadata.name = line.replace('# ', '').trim();
            if (line.startsWith('# Tier:')) metadata.tier = line.split(':')[1].trim();
            if (line.startsWith('# Mode:')) metadata.mode = line.split(':')[1].trim();
        }
        return metadata;
    }

    /**
     * Get an agent by ID.
     * @param {string} agentId - Agent identifier
     * @returns {Object|undefined} Agent object or undefined
     */
    get(agentId) {
        return this.agents.get(agentId);
    }

    /**
     * List all registered agents.
     * @returns {Object[]} Array of agent objects
     */
    list() {
        return Array.from(this.agents.values());
    }

    /**
     * List agents filtered by tier.
     * @param {string} tier - Tier level (T1, T2, T3)
     * @returns {Object[]} Filtered agent array
     */
    listByTier(tier) {
        return this.list().filter(a => a.tier === tier);
    }

    /**
     * Activate an agent (set status to 'active').
     * @param {string} agentId - Agent identifier
     * @returns {Object|undefined} Updated agent or undefined
     */
    activate(agentId) {
        const agent = this.agents.get(agentId);
        if (agent) {
            agent.status = 'active';
            agent.lastActive = new Date().toISOString();
        }
        return agent;
    }

    /**
     * Deactivate an agent (set status to 'available').
     * @param {string} agentId - Agent identifier
     * @returns {Object|undefined} Updated agent or undefined
     */
    deactivate(agentId) {
        const agent = this.agents.get(agentId);
        if (agent) agent.status = 'available';
        return agent;
    }
}

module.exports = { AgentRegistry };
