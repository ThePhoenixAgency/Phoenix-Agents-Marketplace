// Script: Documentation Generator
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Genere la documentation automatiquement a partir du code

const fs = require('fs');
const path = require('path');

/**
 * Generates documentation from source code JSDoc comments
 * and project structure.
 */
class DocGenerator {
    /**
     * @param {string} projectDir - Root project directory
     */
    constructor(projectDir) {
        this.projectDir = projectDir;
    }

    /**
     * Generate a project structure overview.
     * @returns {string} Markdown representation
     */
    generateStructure() {
        const lines = ['# Project Structure', ''];
        const tree = this.buildTree(this.projectDir, 0, 3);
        lines.push(...tree);
        return lines.join('\n');
    }

    /**
     * Build a text tree of the directory.
     * @param {string} dir - Directory to scan
     * @param {number} depth - Current depth
     * @param {number} maxDepth - Maximum depth
     * @returns {string[]} Lines of text
     */
    buildTree(dir, depth, maxDepth) {
        if (depth >= maxDepth) return [];
        const lines = [];
        const indent = '  '.repeat(depth);
        const entries = fs.readdirSync(dir, { withFileTypes: true })
            .filter(e => !['node_modules', '.git', 'coverage', 'dist'].includes(e.name))
            .sort((a, b) => {
                if (a.isDirectory() && !b.isDirectory()) return -1;
                if (!a.isDirectory() && b.isDirectory()) return 1;
                return a.name.localeCompare(b.name);
            });

        for (const entry of entries) {
            if (entry.isDirectory()) {
                lines.push(`${indent}- **${entry.name}/**`);
                lines.push(...this.buildTree(path.join(dir, entry.name), depth + 1, maxDepth));
            } else {
                lines.push(`${indent}- ${entry.name}`);
            }
        }
        return lines;
    }

    /**
     * Count exported functions across all JS/TS files.
     * @param {string} dir - Directory to scan
     * @returns {{ total: number, documented: number }}
     */
    countDocCoverage(dir) {
        let total = 0;
        let documented = 0;
        const files = this.findSourceFiles(dir);

        for (const file of files) {
            const content = fs.readFileSync(file, 'utf8');
            const exports = (content.match(/module\.exports|export (function|class|const)/g) || []).length;
            const jsdoc = (content.match(/\/\*\*/g) || []).length;
            total += exports;
            documented += Math.min(jsdoc, exports);
        }

        return { total, documented };
    }

    /**
     * Find all source files.
     * @param {string} dir - Directory to scan
     * @returns {string[]} File paths
     */
    findSourceFiles(dir) {
        const results = [];
        if (!fs.existsSync(dir)) return results;
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (['node_modules', '.git', 'coverage'].includes(entry.name)) continue;
            if (entry.isDirectory()) {
                results.push(...this.findSourceFiles(fullPath));
            } else if (entry.name.match(/\.(js|ts)$/) && !entry.name.includes('.test.')) {
                results.push(fullPath);
            }
        }
        return results;
    }
}

module.exports = { DocGenerator };
