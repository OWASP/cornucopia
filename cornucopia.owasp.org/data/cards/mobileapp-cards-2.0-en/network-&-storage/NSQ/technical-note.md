## Platform-Aware Review Guidance

**Android**
- `android:usesCleartextTraffic="false"` in `<application>` (or managed via `network_security_config.xml`): blocks all cleartext HTTP traffic.
- Lint: `GetHTTPResource` rule flags `http://` URLs in code; enable in CI.
- Review all hardcoded and dynamically constructed URLs in the source for `http://` scheme usage.
- OkHttp: `OkHttpClient.Builder().protocols(listOf(Protocol.HTTP_2, Protocol.HTTP_1_1))` — both work only over TLS; add `.connectionSpecs(listOf(ConnectionSpec.MODERN_TLS))`.

**iOS**
- ATS: `NSAllowsArbitraryLoads = false` blocks HTTP by default.
- `NSExceptionDomains` entries with `NSExceptionAllowsInsecureHTTPLoads = true` are exceptions that must be documented and justified.
- Audit all URL strings in the code for `http://` patterns.

**Server-Side**
- `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` header on all HTTPS responses.
- Redirect all HTTP requests to HTTPS with a 301 permanent redirect; do not serve API responses over HTTP.

**Testing**
- Proxy all traffic and filter for HTTP requests; verify no app-generated requests use HTTP.
- Use `nmap --script http-methods` to verify the server does not respond to HTTP for sensitive paths.

**OWASP Mappings**
- MASVS: AUTH-1, NETWORK-1
- MASTG: TEST-0019, TEST-0020, TEST-0065, TEST-0066, TEST-0067, TEST-0217, TEST-0218, TEST-0233, TEST-0235, TEST-0236, TEST-0237, TEST-0238, TEST-0239, TEST-0321, TEST-0322, TEST-0323, TEST-0342, TEST-0343, TEST-0344, TEST-0345, TEST-0348
- MASWE: MASWE-0037, MASWE-0050
