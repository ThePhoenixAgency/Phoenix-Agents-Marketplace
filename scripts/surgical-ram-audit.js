#!/usr/bin/env node
const { execSync: ex } = require('child_process');

const run = c => { try { return ex(c, { encoding: 'utf8' }) } catch (e) { return '' } };

const m = () => {
    console.log("--- GROUPED MEMORY ANALYSIS (RSS) ---");
    const ps = run('ps -axo rss,comm').split('\n');
    const groups = {};

    ps.forEach(line => {
        const match = line.trim().match(/^(\d+)\s+(.+)$/);
        if (match) {
            const rss = parseInt(match[1]);
            const cmd = match[2];
            // Simplify command name for grouping (e.g. Google Chrome Helper -> Google Chrome)
            let group = cmd;
            if (cmd.includes('Google Chrome')) group = 'Google Chrome';
            if (cmd.includes('Antigravity')) group = 'Antigravity / Cursor';
            if (cmd.includes('Electron')) group = 'Electron Apps';
            if (cmd.includes('Dropbox')) group = 'Dropbox';
            if (cmd.includes('Slack')) group = 'Slack';
            if (cmd.includes('Ollama')) group = 'Ollama';
            if (cmd.includes('LM Studio')) group = 'LM Studio';

            groups[group] = (groups[group] || 0) + rss;
        }
    });

    const sorted = Object.entries(groups).sort((a, b) => b[1] - a[1]);

    console.log(`${'APPLICATION'.padEnd(40)} | ${'TOTAL_MEM (MB)'.padEnd(15)}`);
    console.log("-".repeat(60));
    sorted.slice(0, 30).forEach(([name, rss]) => {
        console.log(`${name.padEnd(40)} | ${(rss / 1024).toFixed(2).padEnd(15)}`);
    });

    console.log("\n--- SYSTEM PLIST FILES CHECK ---");
    const paths = [
        '~/Library/LaunchAgents',
        '/Library/LaunchAgents',
        '/Library/LaunchDaemons'
    ];
    paths.forEach(p => {
        console.log(`\nContents of ${p} (Non-Apple):`);
        const files = run(`ls -1 ${p} 2>/dev/null`).split('\n').filter(f => f && !f.includes('com.apple'));
        files.forEach(f => console.log(`  - ${f}`));
    });
}; m();
