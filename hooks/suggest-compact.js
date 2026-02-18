// Hook: suggest-compact
// Created: 2026-02-18
// Suggere de compacter le contexte a intervalles reguliers
let editCount = 0;
const COMPACT_THRESHOLD = 50;
module.exports = {
    run(context) {
        editCount++;
        if (editCount >= COMPACT_THRESHOLD) {
            editCount = 0;
            return { status: 'warning', message: `[INFO] ${COMPACT_THRESHOLD} edits since last compact. Consider running /compact.` };
        }
        return { status: 'ok' };
    },
};
