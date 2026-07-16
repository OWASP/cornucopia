## Scenario: Nihel can compromise the communication as it may fall back to an insecure or unencrypted channel, because encryption is optional, or because of client-server protocol or security-provider weaknesses

Consider a scenario where Nihel controls a network appliance between a user and the target app's server. The app negotiates TLS but accepts a downgrade to TLS 1.0 because the server still supports it for "legacy compatibility." Nihel performs a POODLE-style downgrade attack, forcing the connection to TLS 1.0 and exploiting its known weaknesses. The connection was "encrypted" — with a cipher suite that was deprecated in 2015.

1. Apps that accept TLS 1.0 or TLS 1.1 expose users to known protocol downgrade attacks.
2. Apps that allow plaintext fallback (`cleartext traffic permitted`) allow network-level interception on standard Wi-Fi networks.
3. Android security provider vulnerabilities (older versions of Conscrypt/OpenSSL bundled with the app) can be exploited by an on-path attacker.

### Example

Nihel observes the app negotiates `TLS_RSA_WITH_RC4_128_SHA` when connecting to the server — an export-grade cipher that is years past its retirement date. She performs a BEAST/SWEET32 attack against the RC4 session, eventually recovering the session token. The developer's comment in the code reads "// TODO: remove RC4 fallback after server upgrade." The server upgrade was seventeen months ago.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

A downgraded or weak TLS connection provides weaker or no confidentiality guarantees, allowing an on-path attacker to eavesdrop on or modify the communication.

### What can go wrong?

- Protocol downgrade allows exploitation of known weaknesses in older TLS versions or cipher suites.
- Cleartext fallback allows passive interception on any network the user connects to.
- Outdated Android security providers have known cryptographic vulnerabilities.
- HTTP APIs used as a fallback transmit credentials and tokens in cleartext.

### What are we going to do about it?

- Configure the app and server to require TLS 1.2 as a minimum; prefer TLS 1.3.
- Disable all weak cipher suites: no RC4, no 3DES, no export ciphers, no null encryption.
- Set `cleartextTrafficPermitted="false"` in `network_security_config.xml`.
- Keep the Android security provider up to date by calling `ProviderInstaller.installIfNeeded()` at app startup to use the latest Conscrypt from Google Play Services.
