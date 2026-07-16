## Scenario: Pekka can compromise the integrity of the storage because the file integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Pekka modifies the app's local policy configuration file to change the transaction limit from $500 to $50,000. The app reads this file on startup, applies the limits, and then validates the file with a simple CRC32 checksum. Pekka recalculates the CRC32 for his modified file and replaces both the file and the checksum. The app's integrity check passes. Pekka now has a $50,000 transaction limit. The integrity check used a checksum algorithm that any attacker can compute.

1. CRC32 and MD5 are not cryptographic integrity checks; any attacker can compute them for modified content.
2. Symmetric HMAC keys stored on the device are accessible to a root attacker; computing a valid HMAC for modified content requires only the key.
3. File integrity checks that can be bypassed by modifying both the file and the stored hash provide no meaningful protection.

### Example

Pekka finds the app stores a `policy.json` and a `policy.hash` file. The `policy.hash` is an MD5 of `policy.json`. He modifies `policy.json` to increase transfer limits, computes a new MD5, writes both files, and restarts the app. The integrity check reads the hash, computes MD5 of the current file, compares them — they match. The modified policy is applied. The integrity mechanism was defeated by a third-grader with an MD5 implementation and root access.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering**.

Pekka modifies stored policy or configuration data and bypasses the integrity check to make the app accept the modified data as legitimate.

### What can go wrong?

- Transaction limits, security policies, and feature flags stored locally and protected only by a weak checksum are modifiable.
- An attacker modifies the app's SQLite database and passes the weak integrity check, corrupting the app's data.
- Security-relevant configuration is modified to disable security controls.

### What are we going to do about it?

- Use a server-side signature (RSA or ECDSA) over all policy and configuration data; the app verifies the signature using the hardcoded public key.
- Store security policies server-side and fetch them with a verified TLS connection; do not store them in a locally modifiable file.
- For local integrity checks, use HMAC-SHA256 with a key that is hardware-protected (not derivable from on-device information alone).
- Do not store both the file and its integrity value in the same writable location; an attacker with write access to one has write access to both.
