#!/usr/bin/env node
/**
 * Logic Cleaner (The Dishwasher) - Phoenix Project
 * Purifies code fragments by removing non-essential artifacts and normalizing structure.
 * Focused on purity and logic transparency.
 */
const fs = require('fs');
const path = require('path');

const m = () => {
    const a = process.argv.slice(2);
    if (!a.length) return;

    const target = a[0];
    let content = '';

    if (fs.existsSync(target)) {
        content = fs.readFileSync(target, 'utf8');
    } else {
        content = target; // Treat as string fragment
    }

    console.log('\n[PURIFICATION_CYCLE_START]');

    // 1. Strip Comments (removing potential hidden instructions)
    const originalLength = content.length;
    content = content.replace(/\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$/gm, '$1');

    // 2. Remove non-ASCII/Hidden characters (detour protection)
    content = content.replace(/[^\x20-\x7E\n\r\t]/g, '');

    // 3. Normalize Whitespace (flattening logic)
    content = content.replace(/[ \t]+/g, ' ').replace(/\n\s*\n/g, '\n').trim();

    // 4. Fragment Scan (Hex check)
    if (/\\x[0-9a-f]{2}/i.test(content)) {
        console.log(' [!] ANOMALY: Encoded fragments detected after wash. Manual scrutiny required.');
    }

    const saved = originalLength - content.length;
    console.log(` [OK] Cycle complete. Removed ${saved} non-essential characters.`);
    console.log('[CLEAN_LOGIC_PREVIEW]');
    console.log(content.substring(0, 500) + (content.length > 500 ? '...' : ''));

    // Output for pipeline integration if needed
    if (a.includes('--output')) {
        const outPath = target.includes('.') ? target.replace(/(\.[a-z]+)$/, '.clean$1') : 'clean_fragment.txt';
        fs.writeFileSync(outPath, content);
        console.log(`\n [OK] Clean logic saved to: ${outPath}`);
    }
}; m();
