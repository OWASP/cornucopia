## Scenario: Ivan’s Session Identifier Theft

Picture a scenario where Ivan, a savvy attacker, steals session identifiers due to their exposure through various insecure means. He exploits system weaknesses such as:

1. **Transmission over Insecure Channels:** Session identifiers are sent over unencrypted connections.

2. **Logging of Identifiers:** Session IDs are unnecessarily logged in system or application logs.

3. **Exposure in Error Messages:** Identifiers are revealed in verbose error messages.

4. **Inclusion in URLs:** Session IDs are included in URLs, making them vulnerable to exposure.

5. **Accessibility by Attacker-Influenced Code:** Session identifiers are accessible by code or scripts that an attacker can manipulate or alter.

### Example

Ivan targets a web application that transmits session identifiers over HTTP instead of secure HTTPS. He intercepts network traffic and captures these identifiers as they are transmitted unencrypted. Additionally, the application includes session IDs in URL parameters, which can be leaked through browser history or referrer headers. Using these stolen session IDs, Ivan hijacks active user sessions, gaining unauthorized access to their accounts and data.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Spoofing**.

**Spoofing** involves impersonating a legitimate user or entity.
Ivan steals session identifiers through insecure transmission, logging, URL parameters, or code exposure.
By using these stolen session IDs, he hijacks active sessions and impersonates the legitimate user, which is classic **Spoofing**.

### What can go Wrong?

Such practices expose users to session hijacking and potential data breaches, as their session identifiers can be easily intercepted and misused.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Ensure all communication involving session identifiers is encrypted, preferably using HTTPS.
2. Avoid logging session IDs or exposing them in error messages.
3. Refrain from including session identifiers in URLs, opting for more secure methods of transmission.
4. Limit the accessibility of session identifiers in the application’s code, especially to scripts or areas that could be compromised.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
