## Scenario: Ramsey can access stored sensitive data because it is not securely encrypted

Consider a scenario where Ramsey uses ADB to pull a backup from a test device. The health app stores patient records in a SQLite database with no encryption. The database file is readable with SQLite Browser. Ramsey reads every patient record stored on the device. The developer had planned to "add encryption later." Later had not arrived.

1. Sensitive data stored without encryption is readable by anyone with file access.
2. Data stored encrypted but with a hardcoded key provides the appearance of encryption without the security.
3. Data protected only by OS file permissions is readable on rooted/jailbroken devices.

### Example

Ramsey connects a rooted Android device to his computer. He navigates to `/data/data/com.health.app/databases/`. He finds `patients.db`. He opens it with SQLite Browser. Every patient record — name, date of birth, diagnosis, medication — is in plaintext. The developer's comment in the schema file: `// TODO: encrypt database`. The TODO had 47 commits above it without being addressed.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Unencrypted stored sensitive data is readable by any party who can access the storage medium: a rooted device user, a backup reader, a forensics tool, or the next person to own the device.

### What can go wrong?

- Sensitive data (health records, financial details, personal information) is read from an unencrypted database.
- Backup files contain unencrypted sensitive data.
- Regulatory requirements (HIPAA, GDPR) for data encryption at rest are violated.

### What are we going to do about it?

- Encrypt all sensitive data at rest using a key stored in the platform keystore, not derived from the package name or a constant.
- Use SQLCipher for SQLite databases requiring encryption, with the encryption key from the Android `KeyStore` or iOS Keychain.
- Apply the appropriate iOS data protection class (`NSFileProtectionComplete`) to all files containing sensitive data.
- Treat the device's OS-level file permissions as insufficient for sensitive data; apply application-level encryption.
