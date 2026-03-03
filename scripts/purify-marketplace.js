#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const AGENTS_DIR = path.resolve(__dirname, '..', 'agents');
const DEP_DIR = path.join(AGENTS_DIR, 'deprecated');
const KEEP = ['orchestrators', 'tech-lead.md', 'devops-engineer.md', 'security-auditor', 'product-owner.md', 'README.md', 'deprecated'];

if (!fs.existsSync(DEP_DIR)) fs.mkdirSync(DEP_DIR);

fs.readdirSync(AGENTS_DIR).forEach(f => {
    if (KEEP.includes(f) || f.startsWith('.')) return;
    const oldP = path.join(AGENTS_DIR, f);
    const newP = path.join(DEP_DIR, f);
    console.log(`Archiving: ${f}`);
    fs.renameSync(oldP, newP);
});
console.log('Marketplace purified. Only core agents remain active.');
