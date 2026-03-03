#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const SKILLS = path.resolve(__dirname, '..', 'skills');
const R_Z = [
    { n: 'z0', r: /\b(http|https|ftp):\/\//i, s: 'C', d: 'url_det' }, // No URLs allowed in distilled logic
    { n: 'z1', r: /\b(eval|exec|spawn|fork)\b/i, s: 'C', d: 'dyn_ops' }, // Aggressive block on any dynamic op
    { n: 'z2', r: /\b(fetch|axios|request|curl|wget)\b/i, s: 'C', d: 'net_ops' }, // Total network isolation
    { n: 'z3', r: /\.sh|\.bash|\.zsh/i, s: 'H', d: 'sh_ext' }, // Shell script extension detection
    { n: 'z4', r: /\bmkdir|rm|cp|mv\b/i, s: 'H', d: 'fs_mut' } // File system mutation detection
];
const vrf = p => {
    const n = path.basename(p), res = { n, st: 'P', anm: [] }, f = path.join(p, 'SKILL.md');
    if (!fs.existsSync(f)) return { ...res, st: 'F', err: ['ZERO_TRUST_FAIL'] };
    const c = fs.readFileSync(f, 'utf8');
    const scn = (t, l, fl) => { R_Z.forEach(r => { if (r.r.test(t)) { res.anm.push({ n: r.n, s: r.s, l, f: fl, d: r.d }); res.st = 'B'; } }) };
    c.split('\n').forEach((l, i) => scn(l, i + 1));
    fs.readdirSync(p).forEach(file => {
        if (file === 'SKILL.md' || fs.statSync(path.join(p, file)).isDirectory()) return;
        scn(fs.readFileSync(path.join(p, file), 'utf8'), null, file);
    });
    return res;
};
const m = () => {
    const a = process.argv.slice(2); if (!a.length) return;
    const t = a[0] === '--all' ? fs.readdirSync(SKILLS).map(d => path.join(SKILLS, d)) : [path.resolve(SKILLS, a[0])];
    const r = t.filter(p => fs.statSync(p).isDirectory()).map(vrf);
    r.forEach(x => { if (x.st === 'B') { console.log(`[SHADOW] DEVIATION: ${x.n}`); x.anm.forEach(a => console.log(`  ! ${a.d}@${a.l || a.f}`)); } });
    process.exit(0);
}; m();
