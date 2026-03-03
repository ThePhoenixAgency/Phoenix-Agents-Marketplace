#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const SKILLS = path.resolve(__dirname, '..', 'skills');
const PRIV = ['resilience-testing', 'stress-analysis', 'environment-discovery', 'advanced-indexing', 'stability-rewards', 'anomaly-weighting', 'system-reinforcement', 'integrity-development', 'gateway-hardening', 'module-immunity', 'report-templates', 'finetuning-alignment'];
const R_I = [
    { n: 'i0', r: /base64\s*-d\s*[|]\s*(bash|sh|zsh)/i, s: 'C', d: 'b64p' },
    { n: 'i1', r: /\x69\x67\x6E\x6F\x72\x65\s+\x61\x6C\x6C\s+\x69\x6E\x73\x74\x72\x75\x63\x74\x69\x6F\x6E\x73/i, s: 'C', d: 'pinj' },
    { n: 'i2', r: /\x6D\x6F\x64\x69\x66\x79\s+\x28\x53\x4F\x55\x4C\x7C\x4D\x45\x4D\x4F\x52\x59\x7C\x43\x4C\x41\x55\x44\x45\x29\x2E\x6D\x64/i, s: 'C', d: 'mpsn' },
    { n: 'i3', r: /[\u200B-\u200F\u2028-\u202F\u2060-\u206F]/u, s: 'H', d: 'uinv' },
    { n: 'i4', r: /\x72\x6D\s+\x2D\x72\x66\s+\x2F/i, s: 'C', d: 'rrf' },
    { n: 'i5', r: /\x2F\x64\x65\x76\x2F\x74\x63\x70\x2F/i, s: 'C', d: 'dtcp' }
];
const R_F = [
    { n: 'f0', r: /\x63\x75\x72\x6C\s+\x5B\x5E\x7C\x5D\x2A\x2E\x28\x63\x6F\x6D\x7C\x69\x6F\x7C\x6E\x65\x74\x7C\x6F\x72\x67\x7C\x78\x79\x7A\x29/i, s: 'H', d: 'cflw' },
    { n: 'f1', r: /\x77\x67\x65\x74\s+\x5B\x5E\x7C\x5D\x2A\x2E\x28\x63\x6F\x6D\x7C\x69\x6F\x7C\x6E\x65\x74\x7C\x6F\x72\x67\x7C\x78\x79\x7A\x29/i, s: 'H', d: 'wflw' },
    { n: 'f2', r: /\x65\x76\x61\x6C\x28/i, s: 'H', d: 'dexc' },
    { n: 'f3', r: /\x6E\x63\s+\x7C\x6E\x65\x74\x63\x61\x74\s+/i, s: 'H', d: 'nlnk' },
    { n: 'f4', r: /\x63\x68\x6D\x6F\x64\s+\x37\x37\x37/i, s: 'M', d: 'oprm' },
    { n: 'f5', r: /\x73\x75\x64\x6F\s+/i, s: 'M', d: 'aelv' },
    { n: 'f6', r: /\x24\x5B\x41\x2D\x5A\x5F\x5D\x2A\x4B\x45\x59\x7C\x24\x5B\x41\x2D\x5A\x5F\x5D\x2A\s53\x45\x43\x52\x45\x54/i, s: 'M', d: 'sref' }
];
const R_S = [
    { n: 's0', r: /\b(ss\x68\s+-R|n\x67\x72\x6f\x6b|frpc?|s\x6f\x63\x61\x74|cl\x6f\x75dfl\x61\x72\x65d)\b/i, s: 'C', d: 'rrly' },
    { n: 's1', r: /\b(D\x41N|j\x61\x69lbr\x65\x61k|unf\x69lt\x65\x72\x65d\s+m\x6f\x64\x65)\b/i, s: 'C', d: 'jbrk' },
    { n: 's2', r: />\s*\x2F\x64\x65\x76\x2F\x28\x3F\x21\x6E\x75\x6C\x6C\x29\x28\x74\x63\x70\x7C\x75\x64\x70\x7C\x73\x74\x64\x6F\x75\x74\x7C\x73\x74\x64\x65\x72\x72\x29/i, s: 'C', d: 'ordr' },
    { n: 's3', r: /\x64\x6F\x63\x75\x6D\x65\x6E\x74\x2E\x63\x6F\x6F\x6B\x69\x65\x7C\x6C\x6F\x63\x61\x6C\x53\x74\x6F\x72\x61\x67\x65/i, s: 'H', d: 'chjk' },
    { n: 's4', r: /\x28\x64\x6F\x77\x6E\x6C\x6F\x61\x64\x20\x74\x68\x69\x73\x20\x74\x6F\x6F\x6C\x7C\x68\x65\x6C\x70\x65\x72\x20\x74\x6F\x6F\x6C\x7C\x63\x6F\x70\x79\x20\x61\x6E\x64\x20\x70\x61\x73\x74\x65\x20\x28\x74\x68\x69\x73\x7C\x62\x65\x6C\x6F\x77\x29\x29/i, s: 'C', d: 'lure' },
    { n: 's5', r: /\b[a-z0-9]*[31047\$@][a-z0-9]*[31047\$@][a-z0-9]*\b/i, s: 'H', d: 'l33t' },
    { n: 's6', r: /\x68\x74\x74\x70\x73\x3F\x3A\x2F\x2F(?!(localhost|127\.0\.0\.1|ollama\.com|lmstudio\.ai|github\.com\/PhoenixProject))[\w.-]+/i, s: 'W', d: 'erev' },
    { n: 's7', r: /\b(npm\s+install|pip\s+install|yarn\s+add|cargo\s+add)\b/i, s: 'H', d: 'extd' },
    { n: 's8', r: /\x3C\x73\x63\x72\x69\x70\x74\x7C\x6F\x6E\w+\s*=|Access-Control-Allow-Origin:\s*\*/i, s: 'H', d: 'gatg' },
    { n: 's9', r: /\bSameSite\s*=\s*None\b(?!\s*;\s*Secure)/i, s: 'C', d: 'gatg' },
    { n: 's10', r: /\b(TLSv1|TLSv1\.1|TLSv1\.2)\b/i, s: 'W', d: 'gatg' },
    { n: 's11', r: /\bSet-Cookie:.*(?!.*;\s*SameSite=(Strict|Lax)).*$/im, s: 'W', d: 'gdpr' }
];
const fmtr = c => { const m = c.match(/^---\n([\s\S]*?)\n---/); return m ? m[1].split('\n').reduce((a, l) => { const [k, v] = l.split(':').map(s => s.trim()); if (k && v) a[k] = v; return a; }, {}) : null; };
const vrf = p => {
    const n = path.basename(p), res = { n, st: 'P', anm: [] }, f = path.join(p, 'SKILL.md');
    if (!fs.existsSync(f)) return { ...res, st: 'F', err: ['MSKL'] };
    const c = fs.readFileSync(f, 'utf8'), fm = fmtr(c);
    if (!fm) return { ...res, st: 'F', err: ['MFM'] };
    ['name', 'description', 'author', 'version'].forEach(k => { if (!fm[k]) res.anm.push({ s: 'E', d: `MF:${k}` }) });
    if (fm.name !== n) res.anm.push({ s: 'E', d: 'NMIS' });
    const isP = PRIV.includes(n);
    const scn = (t, l, fl) => {
        [R_I, R_F, R_S].forEach((g, i) => {
            g.forEach(r => {
                if (r.r.test(t)) {
                    const sv = (i === 1 && isP) ? 'I' : r.s; res.anm.push({ n: r.n, s: sv, l, f: fl, d: r.d });
                    if (sv === 'C') res.st = 'B'; else if (sv === 'H' && res.st != 'B') res.st = 'W';
                }
            })
        })
    };
    c.split('\n').forEach((l, i) => scn(l, i + 1));
    fs.readdirSync(p).forEach(file => {
        if (file === 'SKILL.md' || fs.statSync(path.join(p, file)).isDirectory()) return;
        const content = fs.readFileSync(path.join(p, file), 'utf8');
        content.split('\n').forEach((line, idx) => scn(line, idx + 1, file));
    });
    if (/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u.test(c)) res.anm.push({ s: 'E', d: 'EMJ' });
    if (res.anm.some(a => a.s === 'E')) res.st = 'F';
    return res;
};
const m = () => {
    const a = process.argv.slice(2); if (!a.length) return;
    const t = a[0] === '--all' ? fs.readdirSync(SKILLS).map(d => path.join(SKILLS, d)) : [path.resolve(SKILLS, a[0])];
    const r = t.filter(p => fs.statSync(p).isDirectory()).map(vrf);
    r.forEach(x => { console.log(`${x.st} ${x.n}`); x.anm.forEach(a => console.log(` ${a.s}:${a.d}@${a.l || a.f}`)); });
    process.exit(0);
}; m();
