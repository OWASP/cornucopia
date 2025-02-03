#  Configuration Architecture
## V1.14.1
Verify the segregation of components of differing trust levels through well-defined security controls, firewall rules, API gateways, reverse proxies, cloud-based security groups, or similar mechanisms.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [923](https://cwe.mitre.org/data/definitions/923)
## V1.14.2
Verify that binary signatures, trusted connections, and verified endpoints are used to deploy binaries to remote devices.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [494](https://cwe.mitre.org/data/definitions/494)
## V1.14.3
Verify that the build pipeline warns of out-of-date or insecure components and takes appropriate actions.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [1104](https://cwe.mitre.org/data/definitions/1104)
## V1.14.4
Verify that the build pipeline contains a build step to automatically build and verify the secure deployment of the application, particularly if the application infrastructure is software defined, such as cloud environment build scripts.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [](https://cwe.mitre.org/data/definitions/)
## V1.14.5
Verify that application deployments adequately sandbox, containerize and/or isolate at the network level to delay and deter attackers from attacking other applications, especially when they are performing sensitive or dangerous actions such as deserialization. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [265](https://cwe.mitre.org/data/definitions/265)
## V1.14.6
Verify the application does not use unsupported, insecure, or deprecated client-side technologies such as NSAPI plugins, Flash, Shockwave, ActiveX, Silverlight, NACL, or client-side Java applets.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [477](https://cwe.mitre.org/data/definitions/477)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
