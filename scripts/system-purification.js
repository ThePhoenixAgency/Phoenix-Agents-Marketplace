#!/usr/bin/env node
/**
 * Phoenix System Purification - Audit & Deep Scrutiny
 * Created: 2026-02-23 | Last Updated: 2026-02-23
 * Standards: Non-destructive Audit, Memory Pressure Detection, English.
 */
const { execSync: ex } = require('child_process');
const fs = require('fs');

const run = c => { try { return ex(c, { encoding: 'utf8', stdio: 'pipe' }) } catch (e) { return '' } };

const m = () => {
    console.log(`\n--- PHOENIX SYSTEM PURIFICATION AUDIT [${new Date().toISOString()}] ---`);

    // 1. RAM Scrutiny
    console.log('\n[RAM_SCRUTINY]');
    const mem = run('ps -rcxo %mem,rss,comm | head -n 20');
    console.log(mem || ' [!] Unable to retrieve memory telemetry.');

    const vm = run('vm_stat');
    if (vm) {
        const pages = vm.split('\n').find(l => l.includes('free:')) || '';
        const free = parseInt(pages.match(/\d+/) || 0) * 4096 / 1024 / 1024;
        console.log(`  VM_FREE_APPROX: ${free.toFixed(2)} MB`);
    }

    // 2. Background Daemons Audit
    console.log('\n[DAEMON_AUDIT]');
    const launch = run('launchctl list | grep -v com.apple | head -n 15');
    console.log(launch || '  No non-Apple daemons identified in immediate scope.');

    // 3. Container & Pod Scrutiny (Deep)
    console.log('\n[CONTAINER_ORPHAN_AUDIT]');
    const dockerAll = run('docker ps -a --format "{{.ID}} {{.Image}} {{.Status}} {{.Size}}"');
    if (dockerAll) {
        dockerAll.split('\n').filter(Boolean).forEach(l => {
            if (l.includes('Exited') || l.includes('Created')) {
                console.log(`  ! ORPHANED: ${l} (Candidate for immediate purge)`);
            } else {
                console.log(`  - ACTIVE: ${l}`);
            }
        });
    } else {
        console.log('  [OFF] Docker service inactive.');
    }

    const pods = run('kubectl get pods -A --no-headers');
    if (pods) {
        console.log('\n[POD_STASIS_AUDIT]');
        pods.split('\n').filter(Boolean).forEach(p => {
            const parts = p.trim().split(/\s+/);
            const status = parts[3];
            if (status !== 'Running') {
                console.log(`  ! DEVIATION: Pod ${parts[1]} is in ${status} state (Check NS:${parts[0]}).`);
            }
        });
    }

    // 4. Memory Purity Advice
    console.log('\n[PURITY_ADVICE]');
    if (mem.includes('Chrome') || mem.includes('Electron')) {
        console.log('  - Identified high RAM footprint from Electron-based components.');
    }
    if (mem.includes('node')) {
        console.log('  - Multiple Node.js segments active. Verify logic alignment.');
    }

    console.log('\n--- PURIFICATION_AUDIT_COMPLETE ---');
    console.log('NOTE: THIS WAS A NON-DESTRUCTIVE AUDIT. NO PROCESSES WERE KILLED.');
}; m();
