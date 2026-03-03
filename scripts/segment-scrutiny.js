#!/usr/bin/env node
/**
 * Segment & Hardware Scrutiny - Phoenix Project
 * Developed for Mac Ultra / Mini-PC environments.
 * Focus: CPU, GPU, Temperature, Identity, and Flux Distribution.
 */
const { execSync: ex } = require('child_process');
const run = c => { try { return ex(c, { encoding: 'utf8', stdio: 'pipe' }) } catch (e) { return '' } };

const m = () => {
    console.log('\n[NODE_IDENTITY]');
    const model = run('sysctl -n hw.model'), cpuBrand = run('sysctl -n machdep.cpu.brand_string');
    console.log(` ID: ${model.trim()} | ${cpuBrand.trim()}`);

    console.log('\n[SEGMENT_STATE]');
    const vs = run('vm_stat'), free = vs.match(/free:\s+(\d+)/), page = vs.match(/page size of (\d+)/);
    if (free && page) console.log(` B_FREE: ${Math.round((parseInt(free[1]) * parseInt(page[1])) / 1024 / 1024)}MB`);

    console.log('\n[THERMAL_METRICS]');
    // Temperature audit (macOS specific thermal level or sensors if available)
    const thermal = run('sysctl -n machdep.xcpm.cpu_thermal_level');
    const fan = run('system_profiler SPFansDataType | grep "Actual Speed" | head -n 1');
    console.log(` THERMAL_LVL: ${thermal.trim() || '0'}`);
    if (fan) console.log(` FAN_SPEED: ${fan.trim().split(': ')[1]}`);

    console.log('\n[FLOW_DISTRIBUTION]');
    const ps = run('ps -rcxo %cpu,%mem,comm | head -n 5');
    console.log(ps.trim() || ' OK');

    // Suspect flow detection (Malware patterns in process list)
    const psFull = run('ps -axo comm,args').toLowerCase();
    const suspect = ['nc', 'netcat', 'ncat', 'ssh -r', 'socat', 'frpc', 'frps', 'ngrok', 'base64 -d'];
    const hits = suspect.filter(s => psFull.includes(s));
    if (hits.length) {
        console.log('\n[SURFACING_ANOMALIES]');
        hits.forEach(h => console.log(` ! NON-LINEAR: ${h}`));
    }
}; m();
