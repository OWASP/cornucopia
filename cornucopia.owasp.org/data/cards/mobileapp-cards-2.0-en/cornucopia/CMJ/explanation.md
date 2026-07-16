## Scenario: Luis can influence or alter cryptographic methods to corrupt other users' data because the integrity of the encrypted data is not verified before being shared with external services

Consider a scenario where Luis intercepts the encrypted data that the target app shares with a cloud sync service. The data is encrypted but not authenticated. Luis modifies a byte of the ciphertext and re-submits it. The cloud service stores the modified ciphertext. When the victim's other devices sync, they receive the corrupted ciphertext, decrypt it, and process the modified data — potentially leading to data corruption, privilege modification, or injection of malicious content into the victim's data store.

1. Sharing encrypted data without an authentication tag allows modification of the ciphertext in transit or at rest.
2. A cloud service that stores whatever it receives becomes a relay for attacker-modified encrypted data.
3. CBC-encrypted data without a MAC is vulnerable to bit-flipping attacks; GCM without verifying the tag allows tag stripping.

### Example

Luis intercepts the sync payload and flips a bit in the encrypted account-role field (from `user` to `admin` using CBC bit-flipping). He re-submits the modified payload. The sync service stores it. The victim's other device syncs and decrypts the modified payload, reading `admin` as the role. The role change takes effect. Luis has elevated the victim's privileges — from his position as a data-in-transit attacker — by exploiting unauthenticated encryption.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering**.

Unverified encrypted data allows Luis to corrupt the victim's data without being detected, relaying the corruption through a trusted cloud service.

### What can go wrong?

- Data modifications in transit corrupt the receiving device's data.
- Privilege or role information is modified through ciphertext manipulation.
- Malicious content is injected into the victim's data store.

### What are we going to do about it?

- Use authenticated encryption (AES-GCM or ChaCha20-Poly1305) for all data shared with external services; always verify the authentication tag before processing the decrypted data.
- Sign the payload with a server-side HMAC or digital signature in addition to encryption; verify the signature on receipt.
- Verify data integrity before applying synced data; reject and discard any data that fails authentication.
