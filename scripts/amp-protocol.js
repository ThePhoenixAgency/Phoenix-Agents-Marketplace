// Script: AMP Protocol (Agent Message Protocol)
// Created: 2026-02-18
// Last Updated: 2026-02-18
// Communication inter-agents signee et structuree

const crypto = require('crypto');

/**
 * Message structure for Agent Message Protocol.
 * Supports signing and verification with RSA keys.
 */
class AMPMessage {
    /**
     * Create a new AMP message.
     * @param {string} from - Sender agent ID
     * @param {string} to - Recipient agent ID ('*' for broadcast)
     * @param {string} type - Message type (request, response, event, etc.)
     * @param {Object} payload - Message data
     */
    constructor(from, to, type, payload) {
        this.id = crypto.randomUUID();
        this.timestamp = new Date().toISOString();
        this.from = from;
        this.to = to;
        this.type = type;
        this.payload = payload;
        this.signature = null;
    }

    /**
     * Sign the message with an RSA private key.
     * @param {string} privateKey - PEM-encoded RSA private key
     * @returns {AMPMessage} this (for chaining)
     */
    sign(privateKey) {
        const data = JSON.stringify({
            id: this.id,
            timestamp: this.timestamp,
            from: this.from,
            to: this.to,
            type: this.type,
            payload: this.payload,
        });
        const sign = crypto.createSign('SHA256');
        sign.update(data);
        this.signature = sign.sign(privateKey, 'hex');
        return this;
    }

    /**
     * Verify the message signature with an RSA public key.
     * @param {string} publicKey - PEM-encoded RSA public key
     * @returns {boolean} true if signature is valid
     */
    verify(publicKey) {
        const data = JSON.stringify({
            id: this.id,
            timestamp: this.timestamp,
            from: this.from,
            to: this.to,
            type: this.type,
            payload: this.payload,
        });
        const verify = crypto.createVerify('SHA256');
        verify.update(data);
        return verify.verify(publicKey, this.signature, 'hex');
    }

    /**
     * Serialize message to plain object.
     * @returns {Object} Plain object representation
     */
    toJSON() {
        return {
            id: this.id,
            timestamp: this.timestamp,
            from: this.from,
            to: this.to,
            type: this.type,
            payload: this.payload,
            signature: this.signature,
        };
    }
}

/**
 * Message bus for inter-agent communication.
 * Supports direct messaging, pub/sub, and broadcast.
 */
class AMPBus {
    constructor() {
        /** @type {Map<string, Function[]>} */
        this.subscribers = new Map();
        /** @type {AMPMessage[]} */
        this.queue = [];
    }

    /**
     * Subscribe an agent to receive messages.
     * @param {string} agentId - Agent ID to subscribe
     * @param {Function} handler - Callback function receiving AMPMessage
     */
    subscribe(agentId, handler) {
        if (!this.subscribers.has(agentId)) {
            this.subscribers.set(agentId, []);
        }
        this.subscribers.get(agentId).push(handler);
    }

    /**
     * Publish a message to its recipient(s).
     * @param {AMPMessage} message - Message to publish
     */
    publish(message) {
        const handlers = this.subscribers.get(message.to) || [];
        for (const handler of handlers) {
            handler(message);
        }
        if (message.to === '*') {
            for (const [agentId, agentHandlers] of this.subscribers) {
                if (agentId !== message.from) {
                    for (const handler of agentHandlers) {
                        handler(message);
                    }
                }
            }
        }
        this.queue.push(message);
    }

    /**
     * Broadcast a message to all agents except the sender.
     * @param {string} from - Sender agent ID
     * @param {string} type - Message type
     * @param {Object} payload - Message data
     */
    broadcast(from, type, payload) {
        const message = new AMPMessage(from, '*', type, payload);
        this.publish(message);
    }
}

module.exports = { AMPMessage, AMPBus };
