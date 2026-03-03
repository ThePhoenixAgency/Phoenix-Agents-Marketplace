/**
 * Build: structural validation of the marketplace project.
 *
 * Created: 2026-02-19
 * Last Updated: 2026-02-23
 *
 * Checks that all declared components exist:
 * - Agents (directories in agents/)
 * - Skills (directories in skills/)
 * - Commands (.sh files in commands/)
 * - Hooks (files in hooks/)
 * - Scripts core (.js files in scripts/)
 * - Schemas (.json files in schemas/)
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
let errors = 0;

/**
 * Checks that a directory exists and contains at least N elements.
 * @param {string} dir - Relative path from ROOT.
 * @param {string} label - Display name.
 * @param {number} minCount - Expected minimum.
 */
function checkDir(dir, label, minCount) {
    const full = path.join(ROOT, dir);
    if (!fs.existsSync(full)) {
        console.error(`  [ERROR] ${label}: directory ${dir}/ missing`);
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

console.log("[BUILD] Validating project structure...\n");

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

// Check required files
const requiredFiles = [
    "README.md",
    "CONTRIBUTING.md",
    "INSTALL.md",
    "LICENSE",
    "CHANGELOG.md",
    "package.json",
    ".gitignore",
];

console.log("\n[BUILD] Required files...");
for (const f of requiredFiles) {
    const full = path.join(ROOT, f);
    if (!fs.existsSync(full)) {
        console.error(`  [ERROR] Missing file: ${f}`);
        errors++;
    }
}
console.log(`  ${requiredFiles.length} files checked`);

// Check marketplace.json
console.log("\n[BUILD] Plugin marketplace.json...");
const marketplacePath = path.join(ROOT, ".claude-plugin", "marketplace.json");
if (fs.existsSync(marketplacePath)) {
    try {
        const data = JSON.parse(fs.readFileSync(marketplacePath, "utf8"));
        if (!data.name) {
            console.error("  [ERROR] marketplace.json: 'name' field missing");
            errors++;
        }
        if (!data.plugins || data.plugins.length === 0) {
            console.error("  [ERROR] marketplace.json: no plugin declared");
            errors++;
        }
        console.log("  [OK] marketplace.json valid");
    } catch (e) {
        console.error(`  [ERROR] marketplace.json: ${e.message}`);
        errors++;
    }
} else {
    console.error("  [ERROR] .claude-plugin/marketplace.json missing");
    errors++;
}

// Result
console.log("");
if (errors > 0) {
    console.error(`[ERROR] Build failed: ${errors} error(s).`);
    process.exit(1);
} else {
    console.log("[OK] Build succeeded: project structure validated.");
}
