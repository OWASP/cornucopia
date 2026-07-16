## Platform-Aware Review Guidance

**Android**
- `network_security_config.xml`: `<base-config cleartextTrafficPermitted="false">` globally disables HTTP.
- OkHttp: configure `ConnectionSpec` to restrict to `ConnectionSpec.MODERN_TLS` (TLS 1.2+, modern cipher suites).
- `ProviderInstaller.installIfNeeded(context)`: updates the security provider at runtime to use the latest version from Google Play Services. Call in `Application.onCreate()`.
- Verify server-supported TLS versions and cipher suites using `testssl.sh` or `ssllabs.com`.

**iOS**
- ATS enforces TLS 1.2+ by default; do not disable ATS (`NSAllowsArbitraryLoads`) in production.
- ATS uses forward-secret cipher suites by default; review `NSExceptionDomains` for any sites with weakened TLS requirements.
- `URLSessionConfiguration.tlsMinimumSupportedProtocolVersion = .TLSv12` as an explicit floor (iOS 13+).

**Testing**
- Use `testssl.sh` against the app's API endpoints to verify no TLS 1.0/1.1 or weak ciphers are accepted.
- Use a proxy to attempt downgrade negotiation to TLS 1.0; verify the app refuses the connection.
- Verify `cleartext traffic permitted="false"` is set and that HTTP URLs are rejected at the network layer.

**OWASP Mappings**
- MASVS: CODE-3, NETWORK-1
- MASTG: TEST-0020, TEST-0023, TEST-0066
- MASWE: MASWE-0048, MASWE-0049, MASWE-0051
