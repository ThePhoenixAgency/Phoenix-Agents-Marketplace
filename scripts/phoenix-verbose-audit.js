#!/usr/bin/env node
/**
 * PHOENIX VERBOSE AUDIT - System Health Report
 * Created: 2026-02-23 | Standards: Phoenix Project
 * State: Non-Destructive Audit
 */

const { execSync: ex } = require('child_process');
const fs = require('fs');
const path = require('path');

const run = c => { try { return ex(c, { encoding: 'utf8', stdio: 'pipe' }) } catch (e) { return '' } };

const formatSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const getDirSize = (p) => {
    try {
        const res = run(`du -sk "${p}"`);
        if (res) return parseInt(res.split('\t')[0]) * 1024;
    } catch (e) { }
    return 0;
};

const m = () => {
    console.log("====================================================");
    console.log("   SYSTEM AUDIT REPORT - PHOENIX PROJECT             ");
    console.log("====================================================");
    console.log(`Date: ${new Date().toISOString()}`);
    console.log("State: Verbose Audit (SAFE / NON-DESTRUCTIVE)");
    console.log("----------------------------------------------------\n");

    // 1. RAM Memory Audit
    console.log("[1] RAM MEMORY ANALYSIS");
    const memRes = run('ps -rcxo %mem,rss,comm | head -n 15');
    if (memRes) {
        console.log("Top 15 memory-consuming processes:");
        console.log(memRes);
    } else {
        console.log(" [!] Unable to retrieve RAM telemetry.");
    }

    const vm = run('vm_stat');
    if (vm) {
        const freePages = parseInt(vm.split('\n').find(l => l.includes('free:'))?.match(/\d+/)?.[0] || 0);
        const speculativePages = parseInt(vm.split('\n').find(l => l.includes('speculative:'))?.match(/\d+/)?.[0] || 0);
        const freeMB = (freePages + speculativePages) * 4096 / 1024 / 1024;
        console.log(`Free RAM (approx): ${freeMB.toFixed(2)} MB`);
        if (freeMB < 500) console.log(" [WARNING] CRITICAL memory pressure detected.");
    }
    console.log("");

    // 2. Heavy Artifacts Audit (.codex)
    console.log("[2] HEAVY DIRECTORIES ANALYSIS");
    const docRoot = path.resolve(__dirname, '..');
    const possibleCodex = [
        path.join(docRoot, '.codex'),
        path.join(process.env.HOME, '.codex'),
        '.codex'
    ];

    let codexFound = false;
    possibleCodex.forEach(p => {
        if (fs.existsSync(p)) {
            const size = getDirSize(p);
            console.log(` [+] .codex directory found: ${p}`);
            console.log(`     Detected size: ${formatSize(size)}`);
            if (size > 100 * 1024 * 1024) console.log("     [!] BLOAT DETECTED: This directory should be purged.");
            codexFound = true;
        }
    });
    if (!codexFound) console.log(" [OK] No large .codex directory found in standard locations.");
    console.log("");

    // 3. Startup Services Audit (LaunchAgents/Daemons)
    console.log("[3] STARTUP ANALYSIS (NON-APPLE)");
    const checkDaemons = (label, daemonPath) => {
        console.log(`   * ${label}:`);
        const files = run(`ls -1 ${daemonPath} 2>/dev/null`).split('\n').filter(f => f && !f.includes('com.apple'));
        if (files.length > 0) {
            files.forEach(f => {
                if (f.includes('earnapp') || f.includes('luminati')) console.log(`     [!] PRIORITY TARGET: ${f}`);
                else console.log(`     - ${f}`);
            });
        } else {
            console.log("     (No third-party services)");
        }
    };
    checkDaemons("User LaunchAgents", "~/Library/LaunchAgents");
    checkDaemons("System LaunchAgents", "/Library/LaunchAgents");
    checkDaemons("System LaunchDaemons", "/Library/Daemons");
    console.log("");

    // 4. Container & Orchestration Audit (Docker/Pods)
    console.log("[4] DOCKER & KUBERNETES ANALYSIS");
    const dockerPs = run('docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.ID}}"');
    if (dockerPs) {
        console.log("Containers found:");
        console.log(dockerPs);
    } else {
        console.log(" [OFF] Docker service inactive or unreachable.");
    }

    const pods = run('kubectl get pods -A --no-headers 2>/dev/null');
    if (pods) {
        console.log("\nKubernetes Pods found:");
        console.log(pods);
    } else {
        console.log(" [OFF] Kubernetes (kubectl) inactive or no Pod detected.");
    }
    console.log("");

    // 5. Scan Trinity Audit (CVE, Local, AI)
    console.log("[5] SCAN TRINITY CHECK");
    const scans = [
        { name: "CVE Scan (Vulnerability)", file: "module-validator.js" },
        { name: "Local Scan (Purity)", file: "daily-health.js" },
        { name: "AI Scan (AIO/Semantic)", file: "seo-scrutiny.js" }
    ];
    scans.forEach(s => {
        const filePath = path.join(__dirname, s.file);
        if (fs.existsSync(filePath)) {
            console.log(` [+] ${s.name}: PRESENT (${s.file})`);
        } else {
            console.log(` [!] ${s.name}: MISSING (Expected: ${s.file})`);
        }
    });

    console.log("\n====================================================");
    console.log("           END OF REPORT - PURGE RECOMMENDED        ");
    console.log("====================================================");
}; m();
