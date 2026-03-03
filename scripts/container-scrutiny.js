#!/usr/bin/env node
/**
 * Container Scrutiny (Volume & Pod Scrutiny) - Phoenix Project
 * Focus: Structural alignment, Resource metrics, and Purity.
 */
const { execSync: ex } = require('child_process');
const run = c => { try { return ex(c, { encoding: 'utf8', stdio: 'pipe' }) } catch (e) { return '' } };
const hasDocker = () => { try { ex('docker version', { stdio: 'ignore' }); return true; } catch (e) { return false; } };

const m = () => {
    console.log('\n[VOLUME_ALIGNMENT]');
    if (!hasDocker()) {
        console.log(' [OFF] Docker service is unreachable or not installed.');
        return;
    }
    const dockerStats = run('docker stats --no-stream --format "{{.Container}} {{.CPUPerc}} {{.MemUsage}}"');
    const dockerPs = run('docker ps --format "{{.ID}} {{.Image}} {{.Status}}"');

    if (dockerPs) {
        console.log(' [CONTAINERS_ACTIVE]');
        const statsMap = dockerStats.split('\n').reduce((acc, l) => {
            const [id, cpu, mem] = l.split(' ');
            if (id) acc[id] = { cpu, mem };
            return acc;
        }, {});

        dockerPs.split('\n').filter(Boolean).forEach(line => {
            const [id, image, status] = line.split(/\s+/);
            const stats = statsMap[id] || { cpu: '?', mem: '?' };
            console.log(`  - ID:${id.slice(0, 8)} [${image}] ${status} | CPU:${stats.cpu} MEM:${stats.mem}`);

            const inspect = run(`docker inspect ${id}`);
            if (inspect.includes('"Privileged": true')) console.log(`    ! NON-LINEAR: Container ${id.slice(0, 8)} is elevated.`);
            if (inspect.includes('"NetworkMode": "host"')) console.log(`    ! NON-LINEAR: Container ${id.slice(0, 8)} has host network access.`);
        });
    } else {
        console.log(' [OFF] No local docker volumes identified.');
    }

    // 2. Pod Scrutiny
    const k8s = run('kubectl get pods -A --no-headers');
    if (k8s) {
        console.log('\n[POD_DISTRIBUTION]');
        k8s.split('\n').filter(Boolean).forEach(p => {
            const parts = p.trim().split(/\s+/);
            const ns = parts[0], name = parts[1], status = parts[3]; // format: NS NAME READY STATUS RESTARTS AGE
            console.log(`  - NS:${ns} [${name.slice(0, 30)}] ${status}`);
            if (status !== 'Running' && status !== 'Completed') console.log(`    ! DEVIATION: Pod ${name} state is ${status}.`);
        });
    }

    // 3. Resource Waste Induction
    const unused = run('docker container ls -a -f status=exited -f status=created --format "{{.ID}} {{.Image}}"');
    if (unused) {
        console.log('\n[RESOURCES_ORPHANED]');
        unused.split('\n').filter(Boolean).forEach(l => console.log(`  - ${l} (Candidate for purge)`));
    }

    console.log('\n[OK] Volume scrutiny cycle complete.');
}; m();
