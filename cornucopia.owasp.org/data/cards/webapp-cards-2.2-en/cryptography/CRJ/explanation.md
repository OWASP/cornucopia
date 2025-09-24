## Scenario: Justin's Access to Unencrypted Credentials

Imagine a scenario where Justin accesses credentials for internal or external resources, services, and other systems because they are stored unencrypted or embedded in source code. This vulnerability arises due to:

1. **Unencrypted Storage of Credentials:** Sensitive credentials are stored in plain text, making them easily accessible.

2. **Credentials Embedded in Source Code:** Important credentials are hard-coded into the application’s source code, posing a significant security risk.

### Example

Justin examines the source code of a publicly accessible repository for a web application and discovers hard-coded credentials for accessing its database. Additionally, he finds that the application stores API keys for external services in unencrypted configuration files. Using these credentials, Justin gains unauthorized access to the application's database and external services, compromising both the application and its integrated systems.

## Threat Modeling

### STRIDE

That scenario clearly maps to **Information Disclosure** in STRIDE.

The primary violation is exposure of sensitive credentials (database passwords, API keys, service credentials).
Once Justin can read those secrets, he can then leverage them for further attacks (like **Tampering**, **Elevation of Privilege**, etc.), but the root threat is that information that should have been protected is disclosed in plaintext or source code.

### What can go Wrong?

Storing credentials in an unencrypted format or embedding them in source code can lead to unauthorized system access, data breaches, and potentially severe security incidents.

### What are you going to do about it?

- Avoid storing credentials in the source code. Instead, use secure vaults or environment variables for credential storage.
- Ensure all sensitive credentials are encrypted and securely managed, accessible only to authorized systems or personnel.
- Regularly audit and update credential management practices to prevent unauthorized access and exposure.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
