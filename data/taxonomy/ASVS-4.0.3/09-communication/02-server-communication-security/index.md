#  Server Communication Security
## V9.2.1
Verify that connections to and from the server use trusted TLS certificates. Where internally generated or self-signed certificates are used, the server must be configured to only trust specific internal CAs and specific self-signed certificates. All others should be rejected.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [295](https://cwe.mitre.org/data/definitions/295)
## V9.2.2
Verify that encrypted communications such as TLS is used for all inbound and outbound connections, including for management ports, monitoring, authentication, API, or web service calls, database, cloud, serverless, mainframe, external, and partner connections. The server must not fall back to insecure or unencrypted protocols.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [319](https://cwe.mitre.org/data/definitions/319)
## V9.2.3
Verify that all encrypted connections to external systems that involve sensitive information or functions are authenticated.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [287](https://cwe.mitre.org/data/definitions/287)
## V9.2.4
Verify that proper certification revocation, such as Online Certificate Status Protocol (OCSP) Stapling, is enabled and configured.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [299](https://cwe.mitre.org/data/definitions/299)
## V9.2.5
Verify that backend TLS connection failures are logged.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [544](https://cwe.mitre.org/data/definitions/544)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
