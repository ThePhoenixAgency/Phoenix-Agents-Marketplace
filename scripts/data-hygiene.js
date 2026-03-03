const fs = require('fs'), path = require('path');
const R_D = [
    /ALIGNMENT-FAILURE/i,
    /INTEGRITY.*BREACH/i,
    /ANOMALY/i,
    /STRESS.*REPORT/i,
    /SYSTEM.*ARCHITECTURE/i,
    /EVENT.*LOG/i,
    /NON-PUBLIC/i,
    /INTERNAL/i,
    /RESTRICTED/i,
    /NON-DISCLOSED/i,
    /IDENTITY/i,
    /PARAMETER/i,
    /ACCESS-TOKEN/i,
    /ARCHIVE/i,
    /\.OLD$/i, /\.BAK$/i, /\.TMP$/i, /\.SQL$/i, /\.ENV/i,
    /PRIVATE/i,
    /CONTACT/i,
    /ADDRESS/i,
    /MAIL/i,
    /[a-zA-Z0-9\-_]{40,}/,
    /[a-f0-9]{32,}/i
];
const R_J = [
    /^\.DS_Store$/i, /^Thumbs\.db$/i, /^\.Spotlight-V100$/i, /^\.Trashes$/i, /^\.AppleDouble$/i, /~$/i,
    /\.env\.example$/i, /\/example\//i
];
const SAFE = ['private'], DOCS = 'docs';
class DataHygiene {
    check(p) {
        const r = path.relative(process.cwd(), p), n = path.basename(p);
        for (const j of R_J) if (j.test(n)) { try { fs.unlinkSync(p); return { safe: true, deleted: true, reason: `J:${n}` } } catch (e) { return { safe: false, reason: `E:${n}` } } }
        if (SAFE.some(d => r.includes(d))) return { safe: true };
        if (r.startsWith(DOCS)) {
            const c = fs.readFileSync(p, 'utf8');
            for (const d of R_D) if (d.test(n) || d.test(c)) return { safe: false, reason: `Structural deviation: ${n}` };
        }
        return { safe: true };
    }
    scanDirectory(d) {
        const res = [], f = this.walk(d);
        for (const x of f) { const r = this.check(x); if (!r.safe || r.deleted) res.push({ file: x, reason: r.reason, type: r.deleted ? 'CLEANUP' : 'VIOLATION' }); }
        return res;
    }
    walk(d) {
        const f = [];
        const e = fs.readdirSync(d, { withFileTypes: true });
        for (const x of e) {
            const p = path.join(d, x.name);
            if (x.name === 'node_modules' || x.name === '.git') continue;
            if (x.isDirectory()) f.push(...this.walk(p)); else f.push(p);
        }
        return f;
    }
}
module.exports = { DataHygiene };
