#!/usr/bin/env node
/**
 * SEO & AI Scrutiny - Phoenix Project
 * Focus: Semantic visibility, robot policies, and metadata integrity.
 */
const fs = require('fs'), path = require('path');
const R = path.resolve(__dirname, '..');

const m = () => {
    console.log('\n[DIGITAL_PRESENCE_AUDIT]');

    // 1. Bot Policy Scrutiny
    const rb = path.join(R, 'robots.txt');
    if (fs.existsSync(rb)) {
        const c = fs.readFileSync(rb, 'utf8');
        console.log(` [OK] robots.txt: ${c.includes('GPTBot') ? 'AI_READY' : 'ALIGNED'}`);
    } else {
        console.log(' [!] MISSING: robots.txt (AI crawlers may be misaligned)');
    }

    // 2. Index Scrutiny
    const sm = path.join(R, 'sitemap.xml');
    if (fs.existsSync(sm)) {
        console.log(' [OK] sitemap.xml: Identified.');
    } else {
        console.log(' [!] MISSING: sitemap.xml');
    }

    // 3. Metadata Scrutiny (README)
    const rd = path.join(R, 'README.md');
    if (fs.existsSync(rd)) {
        const c = fs.readFileSync(rd, 'utf8');
        const hasAIO = /AI|Agent|Phoenix/i.test(c);
        console.log(` [OK] Semantic Quality: ${hasAIO ? 'PURE' : 'MISALIGNED'}`);
    }

    console.log('\n[PRESENCE_STABILIZED]');
}; m();
