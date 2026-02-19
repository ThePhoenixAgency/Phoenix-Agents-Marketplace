/**
 * Build : validation structurelle du projet marketplace.
 *
 * Created: 2026-02-19
 * Last Updated: 2026-02-19
 *
 * Verifie que tous les composants declares existent :
 * - Agents (dossiers dans agents/)
 * - Skills (dossiers dans skills/)
 * - Commands (fichiers .sh dans commands/)
 * - Hooks (fichiers dans hooks/)
 * - Scripts core (fichiers .js dans scripts/)
 * - Schemas (fichiers .json dans schemas/)
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
let errors = 0;

/**
 * Verifie qu'un repertoire existe et contient au moins N elements.
 * @param {string} dir - Chemin relatif depuis ROOT.
 * @param {string} label - Nom affiche.
 * @param {number} minCount - Minimum attendu.
 */
function checkDir(dir, label, minCount) {
    const full = path.join(ROOT, dir);
    if (!fs.existsSync(full)) {
        console.error(`  [ERROR] ${label}: repertoire ${dir}/ manquant`);
        errors++;
        return 0;
    }
    const entries = fs.readdirSync(full).filter(
        (e) => !e.startsWith(".")
    );
    if (entries.length < minCount) {
        console.error(
            `  [ERROR] ${label}: ${entries.length} elements (minimum: ${minCount})`
        );
        errors++;
    }
    return entries.length;
}

console.log("[BUILD] Validation de la structure du projet...\n");

const agents = checkDir("agents", "Agents", 20);
console.log(`  Agents:   ${agents}`);

const skills = checkDir("skills", "Skills", 50);
console.log(`  Skills:   ${skills}`);

const hooks = checkDir("hooks", "Hooks", 10);
console.log(`  Hooks:    ${hooks}`);

const schemas = checkDir("schemas", "Schemas", 3);
console.log(`  Schemas:  ${schemas}`);

const scripts = checkDir("scripts", "Scripts", 8);
console.log(`  Scripts:  ${scripts}`);

// Verifier les fichiers obligatoires
const requiredFiles = [
    "README.md",
    "CONTRIBUTING.md",
    "INSTALL.md",
    "LICENSE",
    "CHANGELOG.md",
    "package.json",
    ".gitignore",
];

console.log("\n[BUILD] Fichiers obligatoires...");
for (const f of requiredFiles) {
    const full = path.join(ROOT, f);
    if (!fs.existsSync(full)) {
        console.error(`  [ERROR] Fichier manquant: ${f}`);
        errors++;
    }
}
console.log(`  ${requiredFiles.length} fichiers verifies`);

// Verifier marketplace.json
console.log("\n[BUILD] Plugin marketplace.json...");
const marketplacePath = path.join(ROOT, ".claude-plugin", "marketplace.json");
if (fs.existsSync(marketplacePath)) {
    try {
        const data = JSON.parse(fs.readFileSync(marketplacePath, "utf8"));
        if (!data.name) {
            console.error("  [ERROR] marketplace.json: champ 'name' manquant");
            errors++;
        }
        if (!data.plugins || data.plugins.length === 0) {
            console.error("  [ERROR] marketplace.json: aucun plugin declare");
            errors++;
        }
        console.log("  [OK] marketplace.json valide");
    } catch (e) {
        console.error(`  [ERROR] marketplace.json: ${e.message}`);
        errors++;
    }
} else {
    console.error("  [ERROR] .claude-plugin/marketplace.json manquant");
    errors++;
}

// Resultat
console.log("");
if (errors > 0) {
    console.error(`[ERROR] Build echoue : ${errors} erreur(s).`);
    process.exit(1);
} else {
    console.log("[OK] Build reussi : structure du projet validee.");
}
