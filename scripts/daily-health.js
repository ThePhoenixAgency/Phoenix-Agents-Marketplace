#!/usr/bin/env node
/**
 * Phoenix System Audit - Multi-Layer Scrutiny
 * Created: 2026-02-23 | Last Updated: 2026-02-23
 * Standards: Non-destructive, Total Visibility, Local-AI Exception (Ollama), English.
 */
const fs = require('fs'), path = require('path'), { execSync: ex } = require('child_process');
const R = path.resolve(__dirname, '..');
const S = {
    v: path.join(__dirname, 'module-validator.js'),
    h: path.join(__dirname, 'data-hygiene.js'),
    s: path.join(__dirname, 'shadow-scrutiny.js'),
    m: path.join(__dirname, 'segment-scrutiny.js'),
    c: path.join(__dirname, 'logic-cleaner.js'),
    j: path.join(__dirname, 'purity-jail.js'),
    o: path.join(__dirname, 'container-scrutiny.js'),
    e: path.join(__dirname, 'seo-scrutiny.js')
};
const P = [{ n: 'Ollama', u: 'http://localhost:11434/api/tags' }, { n: 'LM Studio', u: 'http://localhost:1234/v1/models' }];
const run = c => { try { return { s: true, o: ex(c, { encoding: 'utf8', stdio: 'pipe' }) } } catch (e) { return { s: false, o: (e.stdout || '') + (e.stderr || '') } } };

const chk = async p => {
    try {
        const c = new AbortController(), t = setTimeout(() => c.abort(), 2e3), r = await fetch(p.u, { signal: c.signal });
        clearTimeout(t);
        if (!r.ok) return { st: 'ERR', m: [] };
        const d = await r.json();
        const models = d.models ? d.models.map(m => m.name) : (d.data ? d.data.map(m => m.id) : []);
        return { st: 'ON', m: models };
    } catch (e) { return { st: 'OFF', m: [] } }
};

(async () => {
    const partners = [];
    for (const p of P) { const res = await chk(p); partners.push({ n: p.n, st: res.st, m: res.m }); }
    const hasAI = partners.some(p => p.st === 'ON');

    console.log(`\n--- PHOENIX SYSTEM AUDIT [${new Date().toISOString()}] ---`);
    partners.forEach(p => {
        console.log(` [${p.st}] ${p.n}`);
        if (p.m.length) {
            console.log(`   MODELS: ${p.m.slice(0, 5).join(', ')}${p.m.length > 5 ? '...' : ''}`);
            const dupes = p.m.filter((item, index) => p.m.indexOf(item) !== index);
            if (dupes.length) console.log(`   [ADVICE] Redundant models detected. Consider pruning for segment efficiency.`);
        }
    });

    console.log('\n[MCP_REGISTRY]');
    const mcp = run('ps -axo args | grep mcp | grep -v grep');
    if (mcp.o.trim()) {
        mcp.o.split('\n').filter(Boolean).slice(0, 5).forEach(l => console.log(` [ON] ${l.trim().substring(0, 80)}...`));
    } else {
        console.log(' [OFF] No active MCP servers identified.');
    }

    console.log('\n[NODE_IDENTITY]');
    const seg = run(`node "${S.m}"`);
    seg.o.split('\n').filter(l => /ID:|B_FREE:|THERMAL_|FAN_/.test(l)).forEach(l => console.log(l));

    console.log('\n[LOAD_TELEM]');
    const load = run('ps -rcxo %cpu,%mem,comm | head -n 6');
    console.log(load.o.trim());
    const psLines = load.o.trim().split('\n');
    const highLoadProc = psLines.slice(1).find(l => parseFloat(l.trim().split(/\s+/)[0]) > 40);

    if (highLoadProc) {
        const procName = highLoadProc.trim().split(/\s+/).pop().toLowerCase();
        if (procName.includes('ollama') || procName.includes('llama') || procName.includes('helper') || hasAI) {
            console.log(` [OK] High load attributed to Local AI execution (${procName}).`);
        } else {
            console.log(` ! DEVIATION: High load detected from non-aligned process: ${procName}`);
        }
    }

    console.log('\n[NETWORK_TOPOLOGY]');
    const net = run('lsof -i -P -n | grep LISTEN | head -n 8');
    console.log(net.o.trim() || '  No external listeners identified.');
    if (net.o.includes(':22')) console.log('  [WARN] Remote access gate (SSH) is listening.');

    console.log('\n[VOLUME_METRICS]');
    const df = run('df -h / | tail -n 1');
    console.log(` SYSTEM_DRIVE: ${df.o.trim()}`);
    const volR = run(`node "${S.o}"`);
    const volOut = volR.o.split('\n').filter(l => l.includes('- ID:') || l.includes('- NS:') || l.includes('NON-LINEAR') || l.includes('ORPHANED')).join('\n');
    console.log(volOut || '  Volumes Aligned.');

    console.log('\n[DIGITAL_PRESENCE]');
    const seoR = run(`node "${S.e}"`);
    seoR.o.split('\n').filter(l => l.includes('[OK]') || l.includes('[!]')).forEach(l => console.log(l));

    console.log('\n[LOGIC_ALIGNMENT]');
    const aR = run(`node "${S.v}" --all`);
    console.log(` SKILLS: ${aR.o.includes('B') ? 'DEVIATION' : 'PURE'}\n ${aR.o.split('\n').find(l => l.includes('Result')) || ''}`);

    console.log('\n[PHOENIX_BARRIER]');
    const tools = Object.keys(S).every(k => fs.existsSync(S[k]));
    console.log(` PURITY_GATE: ${tools ? 'ACTIVE' : 'INCOMPLETE'}`);

    console.log('\n[DISK_AUDIT]');
    const artifacts = run('find . -maxdepth 3 -name "*.clean.*" -o -name "*.tmp" -o -name "*.bak" -o -name "*.old"').o.trim();
    if (artifacts) console.log(` ! FRAGMENTS_SIGNALED:\n${artifacts}`);
    else console.log(' [OK] No legacy artifacts identified.');

    console.log('\n--- AUDIT_COMPLETE ---');
})();
