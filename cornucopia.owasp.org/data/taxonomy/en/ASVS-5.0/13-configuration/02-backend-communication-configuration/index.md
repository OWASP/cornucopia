# Backend Communication Configuration

## V13.2.1

Verify that communications between backend application components that don't support the application's standard user session mechanism, including APIs, middleware, and data layers, are authenticated. Authentication must use individual service accounts, short-term tokens, or certificate-based authentication and not unchanging credentials such as passwords, API keys, or shared accounts with privileged access.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113), [115](/taxonomy/capec-3.9/115), [133](/taxonomy/capec-3.9/133), [169](/taxonomy/capec-3.9/169), [179](/taxonomy/capec-3.9/179), [21](/taxonomy/capec-3.9/21), [36](/taxonomy/capec-3.9/36), [37](/taxonomy/capec-3.9/37), [49](/taxonomy/capec-3.9/49), [554](/taxonomy/capec-3.9/554), [57](/taxonomy/capec-3.9/57), [633](/taxonomy/capec-3.9/633), [87](/taxonomy/capec-3.9/87)

## V13.2.2

Verify that communications between backend application components, including local or operating system services, APIs, middleware, and data layers, are performed with accounts assigned the least necessary privileges.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1), [116](/taxonomy/capec-3.9/116), [122](/taxonomy/capec-3.9/122), [126](/taxonomy/capec-3.9/126), [143](/taxonomy/capec-3.9/143), [144](/taxonomy/capec-3.9/144), [149](/taxonomy/capec-3.9/149), [150](/taxonomy/capec-3.9/150), [155](/taxonomy/capec-3.9/155), [169](/taxonomy/capec-3.9/169), [176](/taxonomy/capec-3.9/176), [179](/taxonomy/capec-3.9/179), [180](/taxonomy/capec-3.9/180), [203](/taxonomy/capec-3.9/203), [21](/taxonomy/capec-3.9/21), [215](/taxonomy/capec-3.9/215), [224](/taxonomy/capec-3.9/224), [240](/taxonomy/capec-3.9/240), [37](/taxonomy/capec-3.9/37), [497](/taxonomy/capec-3.9/497), [54](/taxonomy/capec-3.9/54), [541](/taxonomy/capec-3.9/541), [57](/taxonomy/capec-3.9/57), [58](/taxonomy/capec-3.9/58), [75](/taxonomy/capec-3.9/75), [87](/taxonomy/capec-3.9/87)

## V13.2.3

Verify that if a credential has to be used for service authentication, the credential being used by the consumer is not a default credential (e.g., root/root or admin/admin).

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115), [116](/taxonomy/capec-3.9/116), [151](/taxonomy/capec-3.9/151), [16](/taxonomy/capec-3.9/16), [176](/taxonomy/capec-3.9/176), [21](/taxonomy/capec-3.9/21), [37](/taxonomy/capec-3.9/37), [445](/taxonomy/capec-3.9/445), [49](/taxonomy/capec-3.9/49), [554](/taxonomy/capec-3.9/554), [560](/taxonomy/capec-3.9/560), [57](/taxonomy/capec-3.9/57), [70](/taxonomy/capec-3.9/70)

## V13.2.4

Verify that an allowlist is used to define the external resources or systems with which the application is permitted to communicate (e.g., for outbound requests, data loads, or file access). This allowlist can be implemented at the application layer, web server, firewall, or a combination of different layers.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [154](/taxonomy/capec-3.9/154), [176](/taxonomy/capec-3.9/176), [240](/taxonomy/capec-3.9/240), [481](/taxonomy/capec-3.9/481), [57](/taxonomy/capec-3.9/57)

## V13.2.5

Verify that the web or application server is configured with an allowlist of resources or systems to which the server can send requests or load data or files from.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [154](/taxonomy/capec-3.9/154), [240](/taxonomy/capec-3.9/240), [481](/taxonomy/capec-3.9/481), [57](/taxonomy/capec-3.9/57)

## V13.2.6

Verify that where the application connects to separate services, it follows the documented configuration for each connection, such as maximum parallel connections, behavior when maximum allowed connections is reached, connection timeouts, and retry strategies.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [125](/taxonomy/capec-3.9/125), [227](/taxonomy/capec-3.9/227)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
