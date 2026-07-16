## Scenario: Taher can intercept, extract, or modify sensitive data at rest or in transit by influencing or altering methods for transferring or storing data

Consider a scenario where Taher has compromised the app's data-transfer pipeline. The app stores encrypted data locally and periodically syncs it to a cloud service. Taher has found that the app's sync library can be replaced at runtime via a reflection-based plugin system — the plugin is loaded from a directory that is writable on a rooted device. He substitutes a plugin that silently exfiltrates all synced data before encryption. The encryption was correctly implemented. The data was exfiltrated before it reached the encryption layer.

1. Substituting a lower-level library or service used for data transfer allows interception before encryption or after decryption.
2. Writable directories used for plugin or library loading are a code-injection surface on rooted/jailbroken devices.
3. Sync and backup pipelines that handle data differently from the main app may apply weaker security controls.

### Example

Taher identifies that the app's analytics sync module is loaded from a path in the app's external storage directory, which is writable. He replaces the module binary with a version that logs all data passed to `encrypt()` before the encryption call. On the next sync, all plaintext data is logged to a file he controls. The encryption was AES-256-GCM. The pre-encryption hook was not anticipated. "We encrypt everything" was technically true. It was also technically circumvented.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

By altering the methods responsible for data transfer or storage, Taher subverts the security controls that depend on those methods, intercepting data before protection is applied or after it is removed.

### What can go wrong?

- Pre-encryption hooks capture plaintext data before it is protected.
- Post-decryption hooks capture plaintext data after it is decrypted for use.
- Modified transfer functions exfiltrate data to attacker-controlled servers in addition to the legitimate destination.
- Plugin or library loading from writable directories allows runtime code injection.

### What are we going to do about it?

- Never load code or plugins from writable or user-accessible directories in production builds.
- Verify the integrity of all loaded modules using cryptographic signatures before use.
- Apply runtime integrity checks to detect hooking of critical data-handling functions.
- Keep encryption as close to the data source as possible, within a tamper-resistant execution context.
