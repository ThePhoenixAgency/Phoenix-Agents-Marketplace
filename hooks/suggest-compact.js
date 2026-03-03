// Hook: suggest-compact
// @author PhoenixProject
// @created 2026-02-18
// @updated 2026-03-02
//
// Suggere de compacter le contexte a intervalles reguliers pour eviter
// les depassements de fenetre de contexte (200k tokens max).
// Strategie aggressive : compacter avant saturation, pas apres.
//
// Configurable via PHOENIX_COMPACT_THRESHOLD (defaut: 15 modifications)
// Formule : 15 edits * ~2k tokens/edit = ~30k tokens => compaction avant 200k

let editCount = 0;

// Seuil bas = compaction frequente = sessions plus longues sans perte de contexte
const COMPACT_THRESHOLD = parseInt(process.env.PHOENIX_COMPACT_THRESHOLD || '15', 10);

module.exports = {
    run(context) {
        editCount++;
        if (editCount >= COMPACT_THRESHOLD) {
            editCount = 0;
            return {
                status: 'warning',
                message:
                    `[PHOENIX] ${COMPACT_THRESHOLD} modifications depuis le dernier compact.\n` +
                    `[PHOENIX] Lancer /compact pour liberer l'espace contextuel.\n` +
                    `[PHOENIX] (Seuil configurable via PHOENIX_COMPACT_THRESHOLD)`,
            };
        }
        return { status: 'ok' };
    },
};
