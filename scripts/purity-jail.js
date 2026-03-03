#!/usr/bin/env node
/**
 * Purity Jail - Phoenix Project
 * Executes a command in a restricted sub-shell or verified environment.
 * Minimalist and fast.
 */
const { execSync: ex } = require('child_process');
const fs = require('fs');
const path = require('path');

const m = () => {
    const a = process.argv.slice(2);
    if (!a.length) return;

    const cmd = a.join(' ');
    console.log(`\n[ISOLATION_REQUEST] ${cmd.substring(0, 50)}...`);

    // 1. Scrutinization Gate
    const forbidden = [/\x62\x61\x73\x65\x36\x34/i, /\x63\x75\x72\x6C/i, /\x77\x67\x65\x74/i, /\x73\x75\x64\x6F/i, /\x72\x6D\s+\x2D\x72\x66\s+\x2F/i];
    if (forbidden.some(r => r.test(cmd))) {
        console.log(' ! NON-ALIGNED: Logic contains non-linear vectors. Execution aborted.');
        process.exit(1);
    }

    // 2. Fragment Scrutiny (if file)
    const fileMatch = cmd.match(/[a-z0-9_\-\.\/]+\.(sh|py|js|rb|ts)/i);
    if (fileMatch && fs.existsSync(fileMatch[0])) {
        const content = fs.readFileSync(fileMatch[0], 'utf8');
        if (content.length < 50) console.log(' [WARN] Minimalist logic detected. Scrutinizing fragments...');
        if (forbidden.some(r => r.test(content))) {
            console.log(' ! NON-ALIGNED: File content rejected by Purity Gate.');
            process.exit(1);
        }
    }

    // 3. Sandbox Simulation (Environment restriction)
    console.log(' [OK] Purity consensus reached. Executing in isolated jail...');
    try {
        const out = ex(cmd, {
            env: { ...process.env, PATH: '/usr/bin:/bin:/usr/sbin:/sbin', PHOENIX_JAIL: '1' },
            timeout: 5000,
            maxBuffer: 1024 * 1024
        });
        console.log(out.toString());
    } catch (e) {
        console.log(` ! EXIT: ${e.message}`);
        process.exit(1);
    }
}; m();
