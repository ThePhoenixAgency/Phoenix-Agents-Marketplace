// Script: Memory System
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Systeme de memoire persistante pour les sessions

const fs = require('fs');
const path = require('path');

/**
 * Persistent memory system for storing and retrieving
 * session data, agent state, and learned patterns.
 */
class MemorySystem {
    /**
     * @param {string} stateDir - Path to state storage directory
     */
    constructor(stateDir) {
        this.stateDir = stateDir;
        this.ensureDir();
    }

    /** Ensure the state directory exists. */
    ensureDir() {
        if (!fs.existsSync(this.stateDir)) {
            fs.mkdirSync(this.stateDir, { recursive: true });
        }
    }

    /**
     * Save data under a key.
     * @param {string} key - Storage key
     * @param {*} data - Data to store (must be JSON-serializable)
     */
    save(key, data) {
        const filePath = path.join(this.stateDir, `${key}.json`);
        const entry = {
            key,
            data,
            timestamp: new Date().toISOString(),
        };
        fs.writeFileSync(filePath, JSON.stringify(entry, null, 2));
    }

    /**
     * Load data by key.
     * @param {string} key - Storage key
     * @returns {Object|null} Stored entry or null if not found
     */
    load(key) {
        const filePath = path.join(this.stateDir, `${key}.json`);
        if (!fs.existsSync(filePath)) return null;
        const content = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(content);
    }

    /**
     * List all stored keys.
     * @returns {string[]} Array of key names
     */
    list() {
        return fs.readdirSync(this.stateDir)
            .filter(f => f.endsWith('.json'))
            .map(f => f.replace('.json', ''));
    }

    /**
     * Delete a stored key.
     * @param {string} key - Key to delete
     */
    delete(key) {
        const filePath = path.join(this.stateDir, `${key}.json`);
        if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
    }

    /**
     * Save a session summary. Keeps the last 50 sessions.
     * @param {Object} summary - Session summary object
     */
    saveSessionSummary(summary) {
        const existing = this.load('sessions') || { data: [] };
        existing.data.push({
            ...summary,
            timestamp: new Date().toISOString(),
        });
        if (existing.data.length > 50) {
            existing.data = existing.data.slice(-50);
        }
        this.save('sessions', existing.data);
    }
}

module.exports = { MemorySystem };
