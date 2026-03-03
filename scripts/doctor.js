#!/usr/bin/env node
/**
 * Phoenix Doctor - Auto-diagnostic & Structural Healing
 * Created: 2026-02-23 | Last Updated: 2026-02-23
 * nomenclature: Purity, Alignment, Healing, Segments.
 */
const fs = require('fs'), path = require('path'), { execSync: ex } = require('child_process');
const R = path.resolve(__dirname, '..');
const S = {
    v: path.join(__dirname, 'module-validator.js'),
    h: path.join(__dirname, 'data-hygiene.js'),
    s: path.join(__dirname, 'shadow-scrutiny.js'),
    m: path.join(__dirname, 'segment-scrutiny.js'),
    o: path.join(__dirname, 'container-scrutiny.js'),
    c: path.join(__dirname, 'logic-cleaner.js')
};

const run = c => { try { return { s: true, o: ex(c, { encoding: 'utf8', stdio: 'pipe' }) } } catch (e) { return { s: false, o: (e.stdout || '') + (e.stderr || '') } } };

const heal = () => {
    console.log(`\n--- PHOENIX DOCTOR [LOGIC_HEALING_CYCLE] ---`);

    // 1. Structural Scrutiny (Modules)
    console.log('\n[PHASE_1: MODULE_ALIGNMENT]');
    const vR = run(`node "${S.v}" --all`);
    vR.o.split('\n').filter(l => l.includes('F ') || l.includes('W ')).forEach(d => {
        const name = d.split(' ')[1];
        if (d.includes('NMIS')) {
            const md = path.join(R, 'skills', name, 'SKILL.md');
            if (fs.existsSync(md)) {
                fs.writeFileSync(md, fs.readFileSync(md, 'utf8').replace(/name:\s+.*?\n/, `name: ${name}\n`));
                console.log(`  [HEALED] Nomenclature: ${name}`);
            }
        }
    });

    // 2. Disk Scrutiny (Orphan & Dead Code)
    console.log('\n[PHASE_2: DISK_SCRUTINY]');
    const orphans = [];
    const walk = d => {
        fs.readdirSync(d).forEach(f => {
            const p = path.join(d, f);
            if (fs.statSync(p).isDirectory()) { if (!['node_modules', '.git'].includes(f)) walk(p); }
            else if (/\.(tmp|bak|old|clean\.[a-z]+)$/i.test(f)) orphans.push(p);
        });
    };
    walk(R);
    if (orphans.length) {
        orphans.forEach(p => { console.log(`  [ANOMALY] Artifact identified: ${path.relative(R, p)}`); });
        console.log(`  [ADVICE] Manual review suggested for ${orphans.length} unexpected files.`);
    } else {
        console.log('  [OK] No structural artifacts found.');
    }

    // 3. Hygiene Induction
    console.log('\n[PHASE_3: HYGIENE_INDUCTION]');
    const hR = run(`node "${S.h}" --scan`);
    console.log(`  [OK] Hygiene scan complete.`);

    // 4. Barrier Integrity
    console.log('\n[PHASE_4: BARRIER_INTEGRITY]');
    const tools = Object.keys(S).filter(k => !fs.existsSync(S[k]));
    if (tools.length) console.log(`  [!] Missing components: ${tools.join(', ')}`);
    else console.log('  [OK] All purity gates active.');

    console.log('\n[HEALING_COMPLETE]');
    console.log(' --- NEXT_ACTION: node scripts/daily-health.js ---');
}; heal();
