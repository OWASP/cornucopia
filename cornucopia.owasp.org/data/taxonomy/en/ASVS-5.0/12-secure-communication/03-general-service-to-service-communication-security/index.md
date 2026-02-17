# General Service to Service Communication Security

## V12.3.1

Verify that an encrypted protocol such as TLS is used for all inbound and outbound connections to and from the application, including monitoring systems, management tools, remote access and SSH, middleware, databases, mainframes, partner systems, or external APIs. The server must not fall back to insecure or unencrypted protocols.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [31](/taxonomy/capec-3.9/31), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [57](/taxonomy/capec-3.9/57), [593](/taxonomy/capec-3.9/593), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [94](/taxonomy/capec-3.9/94)

## V12.3.2

Verify that TLS clients validate certificates received before communicating with a TLS server.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [57](/taxonomy/capec-3.9/57), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [89](/taxonomy/capec-3.9/89), [94](/taxonomy/capec-3.9/94)

## V12.3.3

Verify that TLS or another appropriate transport encryption mechanism used for all connectivity between internal, HTTP-based services within the application, and does not fall back to insecure or unencrypted communications.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [31](/taxonomy/capec-3.9/31), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [57](/taxonomy/capec-3.9/57), [593](/taxonomy/capec-3.9/593), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [94](/taxonomy/capec-3.9/94)

## V12.3.4

Verify that TLS connections between internal services use trusted certificates. Where internally generated or self-signed certificates are used, the consuming service must be configured to only trust specific internal CAs and specific self-signed certificates.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [57](/taxonomy/capec-3.9/57), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [94](/taxonomy/capec-3.9/94)

## V12.3.5

Verify that services communicating internally within a system (intra-service communications) use strong authentication to ensure that each endpoint is verified. Strong authentication methods, such as TLS client authentication, must be employed to ensure identity, using public-key infrastructure and mechanisms that are resistant to replay attacks. For microservice architectures, consider using a service mesh to simplify certificate management and enhance security.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [115](/taxonomy/capec-3.9/115), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [57](/taxonomy/capec-3.9/57), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [94](/taxonomy/capec-3.9/94)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
