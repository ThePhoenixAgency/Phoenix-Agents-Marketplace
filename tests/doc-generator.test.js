// Tests: Doc Generator
// Created: 2026-02-18

const { DocGenerator } = require('../scripts/doc-generator');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('DocGenerator', () => {
    let tmpDir;
    let generator;

    beforeEach(() => {
        tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'docs-'));
        generator = new DocGenerator(tmpDir);
    });

    afterEach(() => {
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('should generate project structure', () => {
        fs.mkdirSync(path.join(tmpDir, 'src'));
        fs.writeFileSync(path.join(tmpDir, 'src', 'index.js'), '');
        fs.writeFileSync(path.join(tmpDir, 'README.md'), '# Test');

        const structure = generator.generateStructure();
        expect(structure).toContain('Project Structure');
        expect(structure).toContain('src');
    });

    test('should count doc coverage', () => {
        fs.writeFileSync(path.join(tmpDir, 'documented.js'), [
            '/** JSDoc */',
            'module.exports = { foo: 1 };',
        ].join('\n'));
        fs.writeFileSync(path.join(tmpDir, 'undocumented.js'), [
            'module.exports = { bar: 2 };',
        ].join('\n'));

        const coverage = generator.countDocCoverage(tmpDir);
        expect(coverage.total).toBe(2);
        expect(coverage.documented).toBe(1);
    });

    test('should skip test files in source scan', () => {
        fs.writeFileSync(path.join(tmpDir, 'app.js'), 'module.exports = {};');
        fs.writeFileSync(path.join(tmpDir, 'app.test.js'), 'test("x", () => {});');

        const files = generator.findSourceFiles(tmpDir);
        expect(files).toHaveLength(1);
        expect(files[0]).toContain('app.js');
    });

    test('should handle empty directory', () => {
        const structure = generator.generateStructure();
        expect(structure).toContain('Project Structure');
    });

    test('should handle nonexistent directory', () => {
        const gen = new DocGenerator('/nonexistent');
        const files = gen.findSourceFiles('/nonexistent');
        expect(files).toEqual([]);
    });
});
