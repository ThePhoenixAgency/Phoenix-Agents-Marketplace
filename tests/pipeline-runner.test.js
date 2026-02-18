// Tests: Pipeline Runner
// Created: 2026-02-18

const { PipelineRunner } = require('../scripts/pipeline-runner');

describe('PipelineRunner', () => {
    test('should run passing steps', () => {
        const pipeline = new PipelineRunner();
        pipeline.addStep('Echo', 'echo "hello"');
        pipeline.addStep('True', 'true');

        const result = pipeline.run();
        expect(result.passed).toBe(2);
        expect(result.failed).toBe(0);
    });

    test('should detect failing steps', () => {
        const pipeline = new PipelineRunner();
        pipeline.addStep('Pass', 'true');
        pipeline.addStep('Fail', 'false');

        const result = pipeline.run();
        expect(result.passed).toBe(1);
        expect(result.failed).toBe(1);
    });

    test('should stop on failure when option set', () => {
        const pipeline = new PipelineRunner();
        pipeline.addStep('Fail', 'false');
        pipeline.addStep('Never', 'echo "should not run"');

        const result = pipeline.run({ stopOnFailure: true });
        expect(result.failed).toBe(1);
        expect(result.results).toHaveLength(2);
        expect(result.results[1].status).toBe('pending');
    });

    test('should continue after failure by default', () => {
        const pipeline = new PipelineRunner();
        pipeline.addStep('Fail', 'false');
        pipeline.addStep('Pass', 'true');

        const result = pipeline.run();
        expect(result.passed).toBe(1);
        expect(result.failed).toBe(1);
    });

    test('should chain addStep calls', () => {
        const pipeline = new PipelineRunner();
        const result = pipeline.addStep('A', 'true').addStep('B', 'true');
        expect(result).toBe(pipeline);
        expect(pipeline.steps).toHaveLength(2);
    });

    test('should truncate long output', () => {
        const pipeline = new PipelineRunner();
        pipeline.addStep('Long', 'seq 1 1000');

        const result = pipeline.run();
        expect(result.results[0].output.length).toBeLessThanOrEqual(500);
    });

    test('createStandard should build 3 steps', () => {
        const pipeline = PipelineRunner.createStandard();
        expect(pipeline.steps).toHaveLength(3);
        expect(pipeline.steps.map(s => s.name)).toEqual(['Lint', 'Tests', 'Security']);
    });
});
