## Scenario: Emery can access data because it has been obfuscated rather than using an approved cryptographic function

Consider a scenario where Emery downloads the app and decompiles it. He finds that "encrypted" user data is actually Base64-encoded — the developer had called `Base64.encode()` and believed the data was protected. Emery decodes the "encrypted" data in seconds and reads every user's stored profile, including email addresses and birthdays. The encoding was reversible by anyone with internet access.

1. Base64 encoding is not encryption; it is a trivially reversible transformation.
2. XOR-with-fixed-key, ROT13, simple substitution ciphers, and similar "encoding" schemes provide no meaningful confidentiality.
3. Custom "scrambling" functions without a proven cryptographic foundation are security through obscurity.

### Example

Emery finds the app stores "encrypted" passwords as `eval(atob(data))` equivalents — actually just Base64. He decodes the stored values and finds them to be plaintexts. The developer had implemented `encode(password)` as `Base64.encodeToString(password.getBytes())`. This was labelled "encryption" in the code comments. Emery now has every stored credential in plaintext.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Data protected only by encoding (not encryption) provides no meaningful confidentiality guarantee. Anyone who knows or discovers the encoding scheme — which requires no secret — can reverse it.

### What can go wrong?

- "Encrypted" data is trivially decoded by any attacker who examines the stored bytes.
- Security assumptions built on the obfuscation scheme fail immediately when the scheme is discovered.
- Compliance requirements for encryption are not met by encoding.

### What are we going to do about it?

- Use approved, standards-based cryptographic algorithms: AES-256-GCM for symmetric encryption, RSA-OAEP for asymmetric encryption.
- Never use Base64, XOR, ROT13, or similar encoding schemes as a substitute for encryption.
- Store sensitive data encrypted with keys managed by the platform keystore, not derived from constants in the code.
