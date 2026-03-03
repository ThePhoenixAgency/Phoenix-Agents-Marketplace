#!/usr/bin/env bash
# ==============================================================================
# Phoenix Agents Marketplace - Installateur
# @author  EthanBernier
# @team    PhoenixProject
# @version 2.1.0
# @created 2026-02-18
# @updated 2026-03-02
#
# Usage :
#   curl -sSL https://raw.githubusercontent.com/ThePhoenixAgency/Phoenix-Agents-Marketplace/main/install.sh | bash
#   ou : cd Phoenix-Agents-Marketplace && bash install.sh
# ==============================================================================

set -euo pipefail

# -- Configuration -------------------------------------------------------------
readonly REPO_URL="https://github.com/ThePhoenixAgency/Phoenix-Agents-Marketplace.git"
readonly CLAUDE_DIR="$HOME/.claude"
readonly PLUGINS_DIR="$CLAUDE_DIR/plugins"
readonly INSTALL_DIR="$PLUGINS_DIR/phoenix-agents-marketplace"
readonly SETTINGS_FILE="$CLAUDE_DIR/settings.json"
readonly PLUGIN_KEY="phoenix-agents-marketplace@local"

# -- Utilitaires ---------------------------------------------------------------
log()  { echo "[INFO] $*"; }
ok()   { echo "[OK]   $*"; }
warn() { echo "[WARN] $*" >&2; }
die()  { echo "[ERR]  $*" >&2; exit 1; }

# -- Detection de la source ----------------------------------------------------
log "Phoenix Agents Marketplace - Installateur v2.1.0"

if [ -f ".claude-plugin/plugin.json" ]; then
    # Mode local : execution depuis le repo clone
    MARKETPLACE_DIR="$(pwd)"
    log "Mode local : $MARKETPLACE_DIR"
else
    # Mode distant : clone depuis GitHub
    log "Mode distant : clonage depuis GitHub..."
    if [ -d "$INSTALL_DIR" ]; then
        log "Mise a jour installation existante..."
        git -C "$INSTALL_DIR" pull --ff-only || warn "Mise a jour git echouee - installation conservee"
    else
        git clone --depth=1 "$REPO_URL" "$INSTALL_DIR" || die "Echec du clonage"
    fi
    MARKETPLACE_DIR="$INSTALL_DIR"
fi

log "Source : $MARKETPLACE_DIR"
log "Cible  : $PLUGINS_DIR"

# -- Creation du repertoire plugins --------------------------------------------
mkdir -p "$PLUGINS_DIR"

# -- Lien symbolique (leger, pas de copie) -------------------------------------
if [ "$MARKETPLACE_DIR" != "$INSTALL_DIR" ]; then
    [ -L "$INSTALL_DIR" ] || [ -d "$INSTALL_DIR" ] && rm -rf "$INSTALL_DIR"
    ln -s "$MARKETPLACE_DIR" "$INSTALL_DIR"
    ok "Lien symbolique : $MARKETPLACE_DIR -> $INSTALL_DIR"
fi

# -- Enregistrement automatique dans ~/.claude/settings.json ------------------
# Ajoute le plugin dans enabledPlugins s'il est absent
if command -v node >/dev/null 2>&1 && [ -f "$SETTINGS_FILE" ]; then
    node - "$SETTINGS_FILE" "$PLUGIN_KEY" << 'NODESCRIPT'
const fs  = require('fs');
const [,, filePath, pluginKey] = process.argv;

try {
    const raw = fs.readFileSync(filePath, 'utf8');
    const cfg = JSON.parse(raw);

    // Initialisation de la section si absente
    if (!cfg.enabledPlugins) cfg.enabledPlugins = {};

    // Idempotent : ne rien faire si deja present
    if (cfg.enabledPlugins[pluginKey] === true) {
        console.log('[PHOENIX] Plugin deja enregistre : ' + pluginKey);
        process.exit(0);
    }

    // Activation du plugin
    cfg.enabledPlugins[pluginKey] = true;

    // Ecriture avec indentation standard (2 espaces)
    fs.writeFileSync(filePath, JSON.stringify(cfg, null, 2) + '\n', 'utf8');
    console.log('[PHOENIX] Plugin enregistre avec succes : ' + pluginKey);
} catch (err) {
    // Validation de l'entree avant affichage (evite l'injection dans les logs)
    const safe = String(err.message).slice(0, 200).replace(/[^\w\s\-.:\/]/g, '?');
    console.error('[PHOENIX] Erreur settings.json : ' + safe);
    process.exit(1);
}
NODESCRIPT
else
    warn "Node.js absent ou settings.json introuvable"
    warn "Enregistrement manuel requis dans $SETTINGS_FILE :"
    warn "  \"$PLUGIN_KEY\": true"
fi

# -- Verification du contenu installe ------------------------------------------
AGENT_COUNT=$(find "$MARKETPLACE_DIR/agents" -name "*.md" ! -name "README.md" 2>/dev/null | wc -l | xargs)
ORCH_COUNT=$(find "$MARKETPLACE_DIR/agents/orchestrators" -name "*.md" 2>/dev/null | wc -l | xargs)
SKILL_COUNT=$(find "$MARKETPLACE_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l | xargs)
CMD_COUNT=$(find "$MARKETPLACE_DIR/commands" -type f 2>/dev/null | wc -l | xargs)
HOOK_COUNT=$(find "$MARKETPLACE_DIR/hooks" -name "*.js" 2>/dev/null | wc -l | xargs)

echo ""
ok "Installation terminee."
ok "Agents         : $AGENT_COUNT"
ok "Orchestrateurs : $ORCH_COUNT"
ok "Skills         : $SKILL_COUNT"
ok "Commandes      : $CMD_COUNT"
ok "Hooks          : $HOOK_COUNT"
echo ""
log "Redemarrer Claude Code pour activer le plugin."
log "Cle plugin : $PLUGIN_KEY"
