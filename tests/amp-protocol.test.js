// Tests: AMP Protocol
// Created: 2026-02-18

const { AMPMessage, AMPBus } = require('../scripts/amp-protocol');

describe('AMPMessage', () => {
    test('should create a message with required fields', () => {
        const msg = new AMPMessage('agent-a', 'agent-b', 'request', { action: 'test' });

        expect(msg.id).toBeDefined();
        expect(msg.id.length).toBeGreaterThan(0);
        expect(msg.timestamp).toBeDefined();
        expect(msg.from).toBe('agent-a');
        expect(msg.to).toBe('agent-b');
        expect(msg.type).toBe('request');
        expect(msg.payload).toEqual({ action: 'test' });
        expect(msg.signature).toBeNull();
    });

    test('should generate unique IDs for each message', () => {
        const msg1 = new AMPMessage('a', 'b', 'test', {});
        const msg2 = new AMPMessage('a', 'b', 'test', {});

        expect(msg1.id).not.toBe(msg2.id);
    });

    test('should serialize to JSON correctly', () => {
        const msg = new AMPMessage('agent-a', 'agent-b', 'request', { data: 42 });
        const json = msg.toJSON();

        expect(json.id).toBe(msg.id);
        expect(json.from).toBe('agent-a');
        expect(json.to).toBe('agent-b');
        expect(json.type).toBe('request');
        expect(json.payload).toEqual({ data: 42 });
        expect(json.timestamp).toBe(msg.timestamp);
        expect(json.signature).toBeNull();
    });
});

describe('AMPBus', () => {
    let bus;

    beforeEach(() => {
        bus = new AMPBus();
    });

    test('should subscribe and receive messages', () => {
        const received = [];
        bus.subscribe('agent-b', (msg) => received.push(msg));

        const msg = new AMPMessage('agent-a', 'agent-b', 'test', { hello: 'world' });
        bus.publish(msg);

        expect(received).toHaveLength(1);
        expect(received[0].from).toBe('agent-a');
        expect(received[0].payload.hello).toBe('world');
    });

    test('should not deliver messages to wrong agent', () => {
        const received = [];
        bus.subscribe('agent-c', (msg) => received.push(msg));

        const msg = new AMPMessage('agent-a', 'agent-b', 'test', {});
        bus.publish(msg);

        expect(received).toHaveLength(0);
    });

    test('should broadcast to all agents except sender', () => {
        const receivedB = [];
        const receivedC = [];
        const receivedA = [];

        bus.subscribe('agent-a', (msg) => receivedA.push(msg));
        bus.subscribe('agent-b', (msg) => receivedB.push(msg));
        bus.subscribe('agent-c', (msg) => receivedC.push(msg));

        bus.broadcast('agent-a', 'announcement', { text: 'hello all' });

        expect(receivedA).toHaveLength(0);
        expect(receivedB).toHaveLength(1);
        expect(receivedC).toHaveLength(1);
        expect(receivedB[0].payload.text).toBe('hello all');
    });

    test('should store messages in queue', () => {
        const msg1 = new AMPMessage('a', 'b', 'test', {});
        const msg2 = new AMPMessage('a', 'c', 'test', {});

        bus.publish(msg1);
        bus.publish(msg2);

        expect(bus.queue).toHaveLength(2);
    });
});
