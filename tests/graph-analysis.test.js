// Tests: Graph Analysis
// Created: 2026-02-18

const { GraphAnalysis } = require('../scripts/graph-analysis');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('GraphAnalysis', () => {
    let tmpDir;

    beforeEach(() => {
        tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'graph-'));
    });

    afterEach(() => {
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('should build graph from directory', () => {
        fs.writeFileSync(path.join(tmpDir, 'a.js'), "const b = require('./b');\nmodule.exports = {};");
        fs.writeFileSync(path.join(tmpDir, 'b.js'), "module.exports = {};");

        const graph = new GraphAnalysis();
        graph.build(tmpDir);

        expect(graph.graph.size).toBe(2);
        const aImports = graph.graph.get(path.join(tmpDir, 'a.js'));
        expect(aImports.length).toBe(1);
    });

    test('should handle empty directory', () => {
        const graph = new GraphAnalysis();
        graph.build(tmpDir);
        expect(graph.graph.size).toBe(0);
    });

    test('should detect high coupling', () => {
        fs.writeFileSync(path.join(tmpDir, 'hub.js'), [
            "const a = require('./a');",
            "const b = require('./b');",
            "const c = require('./c');",
        ].join('\n'));
        fs.writeFileSync(path.join(tmpDir, 'a.js'), "module.exports = {};");
        fs.writeFileSync(path.join(tmpDir, 'b.js'), "module.exports = {};");
        fs.writeFileSync(path.join(tmpDir, 'c.js'), "module.exports = {};");

        const graph = new GraphAnalysis();
        graph.build(tmpDir);
        const coupling = graph.highCoupling(1);

        expect(coupling[0].file).toContain('hub.js');
        expect(coupling[0].importCount).toBe(3);
    });

    test('should skip node_modules', () => {
        fs.mkdirSync(path.join(tmpDir, 'node_modules'), { recursive: true });
        fs.writeFileSync(path.join(tmpDir, 'node_modules', 'pkg.js'), 'exports.x = 1;');
        fs.writeFileSync(path.join(tmpDir, 'app.js'), 'module.exports = {};');

        const graph = new GraphAnalysis();
        graph.build(tmpDir);

        expect(graph.graph.size).toBe(1);
    });

    test('should handle nonexistent directory', () => {
        const graph = new GraphAnalysis();
        const files = graph.findFiles('/nonexistent', ['.js']);
        expect(files).toEqual([]);
    });

    test('should detect circular dependencies', () => {
        fs.writeFileSync(path.join(tmpDir, 'a.js'), "const b = require('./b');");
        fs.writeFileSync(path.join(tmpDir, 'b.js'), "const a = require('./a');");

        const graph = new GraphAnalysis();
        graph.build(tmpDir);
        const cycles = graph.detectCycles();

        expect(cycles.length).toBeGreaterThan(0);
    });

    test('should return empty array when no cycles', () => {
        fs.writeFileSync(path.join(tmpDir, 'a.js'), "const b = require('./b');");
        fs.writeFileSync(path.join(tmpDir, 'b.js'), "module.exports = {};");

        const graph = new GraphAnalysis();
        graph.build(tmpDir);
        const cycles = graph.detectCycles();

        expect(cycles).toEqual([]);
    });

    test('should parse ES module import syntax', () => {
        fs.writeFileSync(path.join(tmpDir, 'a.js'), "import { foo } from './b';\nexport const x = 1;");
        fs.writeFileSync(path.join(tmpDir, 'b.js'), "export const foo = 42;");

        const graph = new GraphAnalysis();
        graph.build(tmpDir);
        const aImports = graph.graph.get(path.join(tmpDir, 'a.js'));

        expect(aImports.length).toBe(1);
    });

    test('should parse TypeScript files', () => {
        fs.writeFileSync(path.join(tmpDir, 'app.ts'), "import { Service } from './service';");
        fs.writeFileSync(path.join(tmpDir, 'service.ts'), "export class Service {}");

        const graph = new GraphAnalysis();
        graph.build(tmpDir, ['.ts']);

        expect(graph.graph.size).toBe(2);
    });

    test('should ignore external imports', () => {
        fs.writeFileSync(path.join(tmpDir, 'app.js'), [
            "const express = require('express');",
            "const local = require('./local');",
        ].join('\n'));
        fs.writeFileSync(path.join(tmpDir, 'local.js'), "module.exports = {};");

        const graph = new GraphAnalysis();
        graph.build(tmpDir);
        const imports = graph.graph.get(path.join(tmpDir, 'app.js'));

        expect(imports.length).toBe(1);
    });
});
