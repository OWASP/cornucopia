# Backend Communication Configuration

## V13.2.1

Verify that communications between backend application components that don't support the application's standard user session mechanism, including APIs, middleware, and data layers, are authenticated. Authentication must use individual service accounts, short-term tokens, or certificate-based authentication and not unchanging credentials such as passwords, API keys, or shared accounts with privileged access.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113/index.md), [115](/taxonomy/capec-3.9/115/index.md), [133](/taxonomy/capec-3.9/133/index.md), [169](/taxonomy/capec-3.9/169/index.md), [179](/taxonomy/capec-3.9/179/index.md), [21](/taxonomy/capec-3.9/21/index.md), [36](/taxonomy/capec-3.9/36/index.md), [37](/taxonomy/capec-3.9/37/index.md), [49](/taxonomy/capec-3.9/49/index.md), [554](/taxonomy/capec-3.9/554/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md), [87](/taxonomy/capec-3.9/87/index.md)

## V13.2.2

Verify that communications between backend application components, including local or operating system services, APIs, middleware, and data layers, are performed with accounts assigned the least necessary privileges.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1/index.md), [116](/taxonomy/capec-3.9/116/index.md), [122](/taxonomy/capec-3.9/122/index.md), [126](/taxonomy/capec-3.9/126/index.md), [143](/taxonomy/capec-3.9/143/index.md), [144](/taxonomy/capec-3.9/144/index.md), [149](/taxonomy/capec-3.9/149/index.md), [150](/taxonomy/capec-3.9/150/index.md), [155](/taxonomy/capec-3.9/155/index.md), [169](/taxonomy/capec-3.9/169/index.md), [176](/taxonomy/capec-3.9/176/index.md), [179](/taxonomy/capec-3.9/179/index.md), [180](/taxonomy/capec-3.9/180/index.md), [203](/taxonomy/capec-3.9/203/index.md), [21](/taxonomy/capec-3.9/21/index.md), [215](/taxonomy/capec-3.9/215/index.md), [224](/taxonomy/capec-3.9/224/index.md), [240](/taxonomy/capec-3.9/240/index.md), [37](/taxonomy/capec-3.9/37/index.md), [497](/taxonomy/capec-3.9/497/index.md), [54](/taxonomy/capec-3.9/54/index.md), [541](/taxonomy/capec-3.9/541/index.md), [57](/taxonomy/capec-3.9/57/index.md), [58](/taxonomy/capec-3.9/58/index.md), [75](/taxonomy/capec-3.9/75/index.md), [87](/taxonomy/capec-3.9/87/index.md)

## V13.2.3

Verify that if a credential has to be used for service authentication, the credential being used by the consumer is not a default credential (e.g., root/root or admin/admin).

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115/index.md), [116](/taxonomy/capec-3.9/116/index.md), [151](/taxonomy/capec-3.9/151/index.md), [16](/taxonomy/capec-3.9/16/index.md), [176](/taxonomy/capec-3.9/176/index.md), [21](/taxonomy/capec-3.9/21/index.md), [37](/taxonomy/capec-3.9/37/index.md), [445](/taxonomy/capec-3.9/445/index.md), [49](/taxonomy/capec-3.9/49/index.md), [554](/taxonomy/capec-3.9/554/index.md), [560](/taxonomy/capec-3.9/560/index.md), [57](/taxonomy/capec-3.9/57/index.md), [70](/taxonomy/capec-3.9/70/index.md)

## V13.2.4

Verify that an allowlist is used to define the external resources or systems with which the application is permitted to communicate (e.g., for outbound requests, data loads, or file access). This allowlist can be implemented at the application layer, web server, firewall, or a combination of different layers.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [154](/taxonomy/capec-3.9/154/index.md), [176](/taxonomy/capec-3.9/176/index.md), [240](/taxonomy/capec-3.9/240/index.md), [481](/taxonomy/capec-3.9/481/index.md), [57](/taxonomy/capec-3.9/57/index.md)

## V13.2.5

Verify that the web or application server is configured with an allowlist of resources or systems to which the server can send requests or load data or files from.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [154](/taxonomy/capec-3.9/154/index.md), [240](/taxonomy/capec-3.9/240/index.md), [481](/taxonomy/capec-3.9/481/index.md), [57](/taxonomy/capec-3.9/57/index.md)

## V13.2.6

Verify that where the application connects to separate services, it follows the documented configuration for each connection, such as maximum parallel connections, behavior when maximum allowed connections is reached, connection timeouts, and retry strategies.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [125](/taxonomy/capec-3.9/125/index.md), [227](/taxonomy/capec-3.9/227/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
