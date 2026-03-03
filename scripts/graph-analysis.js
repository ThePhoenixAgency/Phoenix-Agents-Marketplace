// Script: Graph Analysis
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Analyzes dependencies between modules and detects cycles

const fs = require('fs');
const path = require('path');

/**
 * Analyses module dependency graphs.
 * Detects circular dependencies and high coupling.
 */
class GraphAnalysis {
    constructor() {
        /** @type {Map<string, string[]>} file -> imports */
        this.graph = new Map();
    }

    /**
     * Build the import graph from a directory.
     * @param {string} dir - Source directory to scan
     * @param {string[]} [extensions=['.js','.ts']] - File extensions
     * @returns {GraphAnalysis} this
     */
    build(dir, extensions = ['.js', '.ts']) {
        const files = this.findFiles(dir, extensions);
        // First pass: register all files
        for (const file of files) {
            this.graph.set(file, []);
        }
        // Second pass: resolve imports against known files
        for (const file of files) {
            const imports = this.extractImports(file);
            this.graph.set(file, imports);
        }
        return this;
    }

    /**
     * Find all files with given extensions.
     * @param {string} dir - Directory to search
     * @param {string[]} extensions - File extensions to include
     * @returns {string[]} Array of file paths
     */
    findFiles(dir, extensions) {
        const results = [];
        if (!fs.existsSync(dir)) return results;
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (entry.name === 'node_modules' || entry.name === '.git') continue;
            if (entry.isDirectory()) {
                results.push(...this.findFiles(fullPath, extensions));
            } else if (extensions.some(ext => entry.name.endsWith(ext))) {
                results.push(fullPath);
            }
        }
        return results;
    }

    /**
     * Extract import paths from a file, resolving to known graph nodes.
     * @param {string} filePath - File to analyze
     * @returns {string[]} Array of resolved imported module paths
     */
    extractImports(filePath) {
        const content = fs.readFileSync(filePath, 'utf8');
        const imports = [];
        const requirePattern = /require\(['"]([^'"]+)['"]\)/g;
        const fromPattern = /from\s+['"]([^'"]+)['"]/g;
        const importPattern = /import\s+['"]([^'"]+)['"]/g;
        const tryExtensions = ['.js', '.ts', '.tsx', '.jsx', ''];

        const processMatch = (importPath) => {
            if (!importPath.startsWith('.')) return;
            const base = path.resolve(path.dirname(filePath), importPath);
            for (const ext of tryExtensions) {
                const candidate = base + ext;
                if (this.graph.has(candidate)) {
                    imports.push(candidate);
                    return;
                }
            }
            imports.push(base);
        };

        let match;
        while ((match = requirePattern.exec(content)) !== null) processMatch(match[1]);
        while ((match = fromPattern.exec(content)) !== null) processMatch(match[1]);
        while ((match = importPattern.exec(content)) !== null) processMatch(match[1]);

        return imports;
    }

    /**
     * Detect circular dependencies in the graph.
     * @returns {string[][]} Array of cycle paths
     */
    detectCycles() {
        const cycles = [];
        const visited = new Set();
        const stack = new Set();

        const dfs = (node, currentPath) => {
            if (stack.has(node)) {
                const cycleStart = currentPath.indexOf(node);
                cycles.push(currentPath.slice(cycleStart));
                return;
            }
            if (visited.has(node)) return;

            visited.add(node);
            stack.add(node);
            currentPath.push(node);

            const deps = this.graph.get(node) || [];
            for (const dep of deps) {
                dfs(dep, [...currentPath]);
            }

            stack.delete(node);
        };

        for (const node of this.graph.keys()) {
            dfs(node, []);
        }

        return cycles;
    }

    /**
     * Get modules with highest coupling (most imports).
     * @param {number} [limit=10] - Max results
     * @returns {{ file: string, importCount: number }[]} Sorted results
     */
    highCoupling(limit = 10) {
        return Array.from(this.graph.entries())
            .map(([file, imports]) => ({ file, importCount: imports.length }))
            .sort((a, b) => b.importCount - a.importCount)
            .slice(0, limit);
    }
}

module.exports = { GraphAnalysis };
