// Tests: Memory System
// Created: 2026-02-18

const { MemorySystem } = require('../scripts/memory-system');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('MemorySystem', () => {
    let tmpDir;
    let memory;

    beforeEach(() => {
        tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'memory-'));
        memory = new MemorySystem(tmpDir);
    });

    afterEach(() => {
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('should create state directory if not exists', () => {
        const newDir = path.join(tmpDir, 'nested', 'state');
        const mem = new MemorySystem(newDir);
        expect(fs.existsSync(newDir)).toBe(true);
    });

    test('should save and load data', () => {
        memory.save('test-key', { value: 42, name: 'test' });
        const loaded = memory.load('test-key');

        expect(loaded).not.toBeNull();
        expect(loaded.key).toBe('test-key');
        expect(loaded.data.value).toBe(42);
        expect(loaded.data.name).toBe('test');
        expect(loaded.timestamp).toBeDefined();
    });

    test('should return null for nonexistent key', () => {
        const result = memory.load('nonexistent');
        expect(result).toBeNull();
    });

    test('should list saved keys', () => {
        memory.save('key-a', { a: 1 });
        memory.save('key-b', { b: 2 });
        memory.save('key-c', { c: 3 });

        const keys = memory.list();
        expect(keys).toHaveLength(3);
        expect(keys).toContain('key-a');
        expect(keys).toContain('key-b');
        expect(keys).toContain('key-c');
    });

    test('should delete a key', () => {
        memory.save('to-delete', { temp: true });
        expect(memory.load('to-delete')).not.toBeNull();

        memory.delete('to-delete');
        expect(memory.load('to-delete')).toBeNull();
    });

    test('should not throw when deleting nonexistent key', () => {
        expect(() => memory.delete('nonexistent')).not.toThrow();
    });

    test('should overwrite existing keys', () => {
        memory.save('key', { version: 1 });
        memory.save('key', { version: 2 });

        const loaded = memory.load('key');
        expect(loaded.data.version).toBe(2);
    });

    test('should save session summaries with limit', () => {
        for (let i = 0; i < 55; i++) {
            memory.saveSessionSummary({ index: i, task: `task-${i}` });
        }

        const sessions = memory.load('sessions');
        expect(sessions).not.toBeNull();
        // Le systeme garde les 50 dernieres
        expect(sessions.data.length).toBeLessThanOrEqual(50);
    });
});
