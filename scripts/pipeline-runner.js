// Script: Pipeline Runner
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Execute les etapes du pipeline de validation

const { execSync } = require('child_process');

/**
 * Runs validation pipeline steps sequentially.
 * Used by CI/CD and the /validate command.
 */
class PipelineRunner {
    constructor() {
        /** @type {{ name: string, command: string, status: string, output: string }[]} */
        this.steps = [];
        this.results = [];
    }

    /**
     * Add a step to the pipeline.
     * @param {string} name - Step name
     * @param {string} command - Shell command to execute
     * @returns {PipelineRunner} this
     */
    addStep(name, command) {
        this.steps.push({ name, command, status: 'pending', output: '' });
        return this;
    }

    /**
     * Run all pipeline steps.
     * @param {{ stopOnFailure: boolean }} [options] - Run options
     * @returns {{ passed: number, failed: number, results: Object[] }}
     */
    run(options = { stopOnFailure: false }) {
        let passed = 0;
        let failed = 0;

        for (const step of this.steps) {
            try {
                const output = execSync(step.command, {
                    timeout: 60000,
                    encoding: 'utf8',
                    stdio: 'pipe',
                });
                step.status = 'passed';
                step.output = output;
                passed++;
            } catch (error) {
                step.status = 'failed';
                step.output = error.stderr || error.message || '';
                failed++;

                if (options.stopOnFailure) break;
            }
        }

        this.results = this.steps.map(s => ({
            name: s.name,
            status: s.status,
            output: s.output.substring(0, 500),
        }));

        return { passed, failed, results: this.results };
    }

    /**
     * Create a standard validation pipeline.
     * @returns {PipelineRunner} Configured pipeline
     */
    static createStandard() {
        const pipeline = new PipelineRunner();
        pipeline.addStep('Lint', 'npm run lint');
        pipeline.addStep('Tests', 'npm test');
        pipeline.addStep('Security', 'npm audit --audit-level=high');
        return pipeline;
    }
}

module.exports = { PipelineRunner };
