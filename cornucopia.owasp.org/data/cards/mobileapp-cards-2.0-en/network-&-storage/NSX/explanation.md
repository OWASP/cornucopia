## Scenario: Maarten can compromise the communication between the app and external services because the app does not verify TLS certificates and chains, trusts insecure sources, lacks hostname verification, or ignores TLS verification issues

Consider a scenario where Maarten is on the same Wi-Fi network as a user of the target app. He performs an ARP spoofing attack to position himself as a man-in-the-middle and presents a self-signed certificate. The app has `X509TrustManager` implemented with empty `checkClientTrusted` and `checkServerTrusted` methods — the classic trust-everything implementation copied from Stack Overflow. Every API call is now transparently proxied through Maarten's machine.

1. Custom `X509TrustManager` implementations that accept all certificates bypass TLS validation entirely.
2. `hostnameVerifier` set to return `true` unconditionally bypasses hostname verification.
3. Setting `CURLOPT_SSL_VERIFYPEER=0` or equivalent in native code disables certificate verification.

### Example

Maarten finds the app was written by a developer who encountered a TLS error in development and "fixed" it by implementing `TrustAllCerts`. The code shipped to production. Maarten presents any self-signed certificate for any hostname. The app connects. He reads and modifies all API traffic, including the authentication endpoint. He intercepts the user's credentials on the first login. The TLS connection was established successfully. No errors were raised. The security indicator in the app showed a lock icon.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

Disabling TLS certificate or hostname verification eliminates the authentication property of TLS, allowing any party who can intercept the network connection to read and modify all traffic.

### What can go wrong?

- Credentials, session tokens, and all sensitive API traffic are intercepted.
- API responses are modified to inject malicious content or grant additional access.
- The user and the app have no indication the connection is being intercepted.

### What are we going to do about it?

- Never implement `X509TrustManager` with empty check methods; use the default system trust manager.
- Never set `HostnameVerifier` to `ALLOW_ALL_HOSTNAME_VERIFIER` or a lambda that returns `true`.
- Use linting rules or static analysis (Android Lint rule `TrustAllX509TrustManager`) to flag insecure TLS configurations at build time.
- Test TLS configuration with a proxy; verify the app rejects self-signed certificates and certificates for incorrect hostnames.
