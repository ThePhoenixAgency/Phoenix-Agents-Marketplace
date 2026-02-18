// Tests: AMP Protocol - sign/verify
// Created: 2026-02-18

const crypto = require('crypto');
const { AMPMessage } = require('../scripts/amp-protocol');

describe('AMPMessage signing', () => {
    let privateKey;
    let publicKey;

    beforeAll(() => {
        const keyPair = crypto.generateKeyPairSync('rsa', {
            modulusLength: 2048,
            publicKeyEncoding: { type: 'spki', format: 'pem' },
            privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
        });
        privateKey = keyPair.privateKey;
        publicKey = keyPair.publicKey;
    });

    test('should sign a message', () => {
        const msg = new AMPMessage('a', 'b', 'test', { data: 'hello' });
        expect(msg.signature).toBeNull();

        msg.sign(privateKey);
        expect(msg.signature).not.toBeNull();
        expect(msg.signature.length).toBeGreaterThan(0);
    });

    test('should verify a valid signature', () => {
        const msg = new AMPMessage('a', 'b', 'test', { data: 'secure' });
        msg.sign(privateKey);

        expect(msg.verify(publicKey)).toBe(true);
    });

    test('should reject a tampered message', () => {
        const msg = new AMPMessage('a', 'b', 'test', { data: 'original' });
        msg.sign(privateKey);

        // Tamper with the payload
        msg.payload.data = 'tampered';

        expect(msg.verify(publicKey)).toBe(false);
    });

    test('should reject a wrong key', () => {
        const msg = new AMPMessage('a', 'b', 'test', { data: 'hello' });
        msg.sign(privateKey);

        const otherKeyPair = crypto.generateKeyPairSync('rsa', {
            modulusLength: 2048,
            publicKeyEncoding: { type: 'spki', format: 'pem' },
            privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
        });

        expect(msg.verify(otherKeyPair.publicKey)).toBe(false);
    });
});
