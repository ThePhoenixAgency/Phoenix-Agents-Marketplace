/**
 * Lint: project structure and syntax validation.
 *
 * Created: 2026-02-19
 * Last Updated: 2026-02-23
 *
 * Checks:
 * - Valid JSON (schemas, marketplace.json, package.json)
 * - Shell syntax (bash -n on all .sh)
 * - JavaScript syntax (node --check on all .js)
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const os = require("os");

const ROOT = path.resolve(__dirname, "..");
let errors = 0;

/**
 * Recursively collects files with the given extension.
 * @param {string} dir - Starting directory.
 * @param {string} ext - Extension (e.g. ".json").
 * @returns {string[]} List of absolute paths.
 */
function collectFiles(dir, ext) {
    const results = [];
    if (!fs.existsSync(dir)) return results;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.name === "node_modules" || entry.name === ".git"
            || entry.name === ".venv" || entry.name === "coverage") {
            continue;
        }
        if (entry.isDirectory()) {
            results.push(...collectFiles(full, ext));
        } else if (entry.name.endsWith(ext)) {
            results.push(full);
        }
    }
    return results;
}

// -- JSON syntax --
console.log("[LINT] JSON syntax check...");
const jsonFiles = collectFiles(ROOT, ".json").filter(
    (f) => !f.includes("node_modules") && !f.includes("package-lock")
);
for (const f of jsonFiles) {
    try {
        JSON.parse(fs.readFileSync(f, "utf8"));
    } catch (e) {
        console.error(`  [ERROR] ${path.relative(ROOT, f)}: ${e.message}`);
        errors++;
    }
}
console.log(`  ${jsonFiles.length} valid JSON files`);

// -- Shell syntax (bash -n) --
console.log("[LINT] Shell syntax check...");
const shFiles = collectFiles(path.join(ROOT, "commands"), ".sh");
for (const f of shFiles) {
    try {
        execSync(`bash -n "${f}"`, { stdio: "pipe" });
    } catch (e) {
        console.error(`  [ERROR] ${path.relative(ROOT, f)}: syntax error`);
        errors++;
    }
}
console.log(`  ${shFiles.length} valid shell scripts`);

// -- JavaScript syntax (node --check) --
console.log("[LINT] JavaScript syntax check...");
const jsFiles = collectFiles(path.join(ROOT, "scripts"), ".js");
for (const f of jsFiles) {
    try {
        execSync(`node --check "${f}"`, { stdio: "pipe" });
    } catch (e) {
        console.error(`  [ERROR] ${path.relative(ROOT, f)}: syntax error`);
        errors++;
    }
}
console.log(`  ${jsFiles.length} valid JS scripts`);

// -- Python syntax (python3 -m py_compile) --
console.log("[LINT] Python syntax check...");
const pyFiles = collectFiles(ROOT, ".py");
let pyCacheDir = null;
const compilePython = (file) => {
    const envPrefix = pyCacheDir ? `PYTHONPYCACHEPREFIX="${pyCacheDir}" ` : "";
    execSync(`${envPrefix}python3 -m py_compile "${file}"`, { stdio: "pipe" });
};
const ensurePyCache = () => {
    if (pyCacheDir) return;
    pyCacheDir = fs.mkdtempSync(path.join(os.tmpdir(), "codex-py-cache-"));
};
try {
    for (const f of pyFiles) {
        try {
            compilePython(f);
        } catch (e) {
            const msg = (e.stderr || e.stdout || "").toString();
            if (/Operation not permitted/.test(msg) && !pyCacheDir) {
                ensurePyCache();
                compilePython(f);
                continue;
            }
            console.error(`  [ERROR] ${path.relative(ROOT, f)}: syntax error`);
            errors++;
        }
    }
} finally {
    if (pyCacheDir) fs.rmSync(pyCacheDir, { recursive: true, force: true });
}
console.log(`  ${pyFiles.length} valid Python scripts`);

// -- Result --
if (errors > 0) {
    console.error(`\n[ERROR] ${errors} lint error(s) detected.`);
    process.exit(1);
} else {
    console.log(`\n[OK] Lint clean: ${jsonFiles.length + shFiles.length + jsFiles.length + pyFiles.length} files checked.`);
}
