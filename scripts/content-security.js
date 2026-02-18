// Script: Content Security
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Verification que les documents sensibles ne sont pas dans les commits

const fs = require('fs');
const path = require('path');

/** Patterns that indicate sensitive content. */
const SENSITIVE_PATTERNS = [
    /THREAT[-_]MODEL/i,
    /REMEDIATION.*REPORT/i,
    /VULNERABILITY/i,
    /AUDIT.*REPORT/i,
    /SECURITY.*ARCHITECTURE/i,
    /INCIDENT.*RESPONSE/i,
    /CONFIDENTIAL/i,
    /INTERNAL/i,
    /RESTRICTED/i,
];

const SAFE_DIRECTORIES = ['private'];
const DOCS_DIR = 'docs';

/**
 * Checks files for sensitive content that should not
 * be committed to public repositories.
 */
class ContentSecurity {
    /**
     * Check a single file for sensitive content.
     * Files in /private/ are always safe.
     * Files in /docs/ are checked against SENSITIVE_PATTERNS.
     * @param {string} filePath - Absolute path to file
     * @returns {{ safe: boolean, reason?: string }}
     */
    check(filePath) {
        const relativePath = path.relative(process.cwd(), filePath);
        const inDocs = relativePath.startsWith(DOCS_DIR);
        const inPrivate = SAFE_DIRECTORIES.some(d => relativePath.includes(d));

        if (inPrivate) return { safe: true };

        if (inDocs) {
            const content = fs.readFileSync(filePath, 'utf8');
            const fileName = path.basename(filePath);

            for (const pattern of SENSITIVE_PATTERNS) {
                if (pattern.test(fileName) || pattern.test(content)) {
                    return {
                        safe: false,
                        reason: `Sensitive content detected: ${pattern}. Move to /private/.`,
                    };
                }
            }
        }

        return { safe: true };
    }

    /**
     * Scan an entire directory tree for violations.
     * @param {string} dir - Root directory to scan
     * @returns {{ file: string, reason: string }[]} Array of violations
     */
    scanDirectory(dir) {
        const results = [];
        const files = this.walkDir(dir);

        for (const file of files) {
            const result = this.check(file);
            if (!result.safe) {
                results.push({ file, reason: result.reason });
            }
        }

        return results;
    }

    /**
     * Recursively walk a directory tree.
     * Skips node_modules and .git.
     * @param {string} dir - Directory to walk
     * @returns {string[]} Array of file paths
     */
    walkDir(dir) {
        const files = [];
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (entry.name === 'node_modules' || entry.name === '.git') continue;
            if (entry.isDirectory()) {
                files.push(...this.walkDir(fullPath));
            } else {
                files.push(fullPath);
            }
        }
        return files;
    }
}

module.exports = { ContentSecurity };
