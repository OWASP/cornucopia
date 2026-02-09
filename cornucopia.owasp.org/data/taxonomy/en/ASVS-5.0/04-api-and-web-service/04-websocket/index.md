# WebSocket

## V4.4.1

Verify that WebSocket over TLS (WSS) is used for all WebSocket connections.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102/index.md), [117](/taxonomy/capec-3.9/117/index.md), [383](/taxonomy/capec-3.9/383/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V4.4.2

Verify that, during the initial HTTP WebSocket handshake, the Origin header field is checked against a list of origins allowed for the application.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [383](/taxonomy/capec-3.9/383/index.md), [62](/taxonomy/capec-3.9/62/index.md)

## V4.4.3

Verify that, if the application's standard session management cannot be used, dedicated tokens are being used for this, which comply with the relevant Session Management security requirements.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [21](/taxonomy/capec-3.9/21/index.md), [383](/taxonomy/capec-3.9/383/index.md), [49](/taxonomy/capec-3.9/49/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V4.4.4

Verify that dedicated WebSocket session management tokens are initially obtained or validated through the previously authenticated HTTPS session when transitioning an existing HTTPS session to a WebSocket channel.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115/index.md), [383](/taxonomy/capec-3.9/383/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
