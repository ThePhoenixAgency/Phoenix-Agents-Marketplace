/**
 * Lint : validation de la structure et syntaxe du projet.
 *
 * Created: 2026-02-19
 * Last Updated: 2026-02-19
 *
 * Verifie :
 * - JSON valide (schemas, marketplace.json, package.json)
 * - Shell syntax (bash -n sur tous les .sh)
 * - JavaScript syntax (node --check sur tous les .js)
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
let errors = 0;

/**
 * Collecte recursivement les fichiers avec l'extension donnee.
 * @param {string} dir - Repertoire de depart.
 * @param {string} ext - Extension (ex: ".json").
 * @returns {string[]} Liste de chemins absolus.
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
console.log(`  ${jsonFiles.length} fichiers JSON valides`);

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
console.log(`  ${shFiles.length} scripts shell valides`);

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
console.log(`  ${jsFiles.length} scripts JS valides`);

// -- Python syntax (python3 -m py_compile) --
console.log("[LINT] Python syntax check...");
const pyFiles = collectFiles(ROOT, ".py");
for (const f of pyFiles) {
    try {
        execSync(`python3 -m py_compile "${f}"`, { stdio: "pipe" });
    } catch (e) {
        console.error(`  [ERROR] ${path.relative(ROOT, f)}: syntax error`);
        errors++;
    }
}
console.log(`  ${pyFiles.length} scripts Python valides`);

// -- Resultat --
if (errors > 0) {
    console.error(`\n[ERROR] ${errors} erreur(s) de lint detectee(s).`);
    process.exit(1);
} else {
    console.log(`\n[OK] Lint clean : ${jsonFiles.length + shFiles.length + jsFiles.length + pyFiles.length} fichiers verifies.`);
}
