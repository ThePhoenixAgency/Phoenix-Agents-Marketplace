// Tests: Session Start Hook - full package manager detection
// Created: 2026-02-18

const sessionStart = require('../hooks/session-start');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('session-start package manager detection', () => {
    let tmpDir;

    beforeEach(() => {
        tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pkgmgr-'));
    });

    afterEach(() => {
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('should detect npm', () => {
        fs.writeFileSync(path.join(tmpDir, 'package-lock.json'), '{}');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('npm');
    });

    test('should detect yarn', () => {
        fs.writeFileSync(path.join(tmpDir, 'yarn.lock'), '');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('yarn');
    });

    test('should detect pnpm', () => {
        fs.writeFileSync(path.join(tmpDir, 'pnpm-lock.yaml'), '');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('pnpm');
    });

    test('should detect bun', () => {
        fs.writeFileSync(path.join(tmpDir, 'bun.lockb'), '');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('bun');
    });

    test('should detect bundler', () => {
        fs.writeFileSync(path.join(tmpDir, 'Gemfile.lock'), '');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('bundler');
    });

    test('should detect poetry', () => {
        fs.writeFileSync(path.join(tmpDir, 'poetry.lock'), '');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('poetry');
    });

    test('should detect go', () => {
        fs.writeFileSync(path.join(tmpDir, 'go.sum'), '');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('go');
    });

    test('should detect cargo', () => {
        fs.writeFileSync(path.join(tmpDir, 'Cargo.lock'), '');
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBe('cargo');
    });

    test('should return null for unknown project', () => {
        const result = sessionStart.run({ projectDir: tmpDir });
        expect(result.data.packageManager).toBeNull();
    });

    test('should use cwd if projectDir not provided', () => {
        const result = sessionStart.run({});
        expect(result.status).toBe('ok');
        expect(result.data.projectDir).toBeDefined();
    });
});
