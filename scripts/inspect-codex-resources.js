#!/usr/bin/env node
const { execSync: ex } = require('child_process');
const fs = require('fs');
const path = require('path');

const run = c => { try { return ex(c, { encoding: 'utf8', stdio: 'pipe' }) } catch (e) { return '' } };

const m = () => {
    const codexPath = path.join(process.env.HOME || process.env.USERPROFILE, '.codex');
    console.log(`\n--- INSPECTING CONTENTS OF: ${codexPath} ---`);

    if (fs.existsSync(codexPath)) {
        // List top-level directories and their size
        const items = fs.readdirSync(codexPath);
        items.forEach(item => {
            const p = path.join(codexPath, item);
            const stats = fs.statSync(p);
            const isDir = stats.isDirectory();
            const sizeRes = run(`du -sh "${p}"`).split('\t')[0];
            console.log(`  [${isDir ? 'DIR' : 'FILE'}] ${item.padEnd(30)} | Size: ${sizeRes}`);
        });
    } else {
        console.log(" [!] .codex directory not found.");
    }

    console.log('\n--- DETAILED CONTAINERS AND PODS ---');
    const dockers = run('docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}"');
    console.log('\n[DOCKER_CONTAINERS]');
    console.log(dockers || '  No container found.');

    const pods = run('kubectl get pods -A -o wide');
    console.log('\n[KUBERNETES_PODS]');
    console.log(pods || '  No Pod found.');

    console.log('\n--- END OF INSPECTION ---');
}; m();
