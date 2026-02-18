// Tests: Content Security
// Created: 2026-02-18

const { ContentSecurity } = require('../scripts/content-security');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('ContentSecurity', () => {
    let tmpDir;
    let security;
    let originalCwd;

    beforeEach(() => {
        tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'security-'));
        fs.mkdirSync(path.join(tmpDir, 'docs'), { recursive: true });
        fs.mkdirSync(path.join(tmpDir, 'private'), { recursive: true });
        fs.mkdirSync(path.join(tmpDir, 'src'), { recursive: true });

        security = new ContentSecurity();
        originalCwd = process.cwd;
        process.cwd = () => tmpDir;
    });

    afterEach(() => {
        process.cwd = originalCwd;
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('should allow files in private directory', () => {
        const filePath = path.join(tmpDir, 'private', 'THREAT-MODEL.md');
        fs.writeFileSync(filePath, 'Secret threat model content');

        const result = security.check(filePath);
        expect(result.safe).toBe(true);
    });

    test('should block sensitive file names in docs', () => {
        const filePath = path.join(tmpDir, 'docs', 'THREAT-MODEL.md');
        fs.writeFileSync(filePath, 'Public threat model');

        const result = security.check(filePath);
        expect(result.safe).toBe(false);
        expect(result.reason).toContain('Sensitive');
    });

    test('should block sensitive content in docs', () => {
        const filePath = path.join(tmpDir, 'docs', 'readme.md');
        fs.writeFileSync(filePath, 'This is CONFIDENTIAL information');

        const result = security.check(filePath);
        expect(result.safe).toBe(false);
    });

    test('should allow safe files in docs', () => {
        const filePath = path.join(tmpDir, 'docs', 'README.md');
        fs.writeFileSync(filePath, 'This is a normal readme file');

        const result = security.check(filePath);
        expect(result.safe).toBe(true);
    });

    test('should allow files outside docs', () => {
        const filePath = path.join(tmpDir, 'src', 'index.js');
        fs.writeFileSync(filePath, 'console.log("hello")');

        const result = security.check(filePath);
        expect(result.safe).toBe(true);
    });

    test('should scan directory and find violations', () => {
        fs.writeFileSync(path.join(tmpDir, 'docs', 'safe.md'), 'Normal content');
        fs.writeFileSync(path.join(tmpDir, 'docs', 'VULNERABILITY-REPORT.md'), 'Found XSS');
        fs.writeFileSync(path.join(tmpDir, 'src', 'app.js'), 'const x = 1;');

        const results = security.scanDirectory(tmpDir);
        expect(results.length).toBeGreaterThanOrEqual(1);
        expect(results.some(r => r.file.includes('VULNERABILITY'))).toBe(true);
    });
});
