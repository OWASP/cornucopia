## Scenario: Alison’s Manipulation Across Domains

Visualize a situation where Alison, exploiting weaknesses in cookie or token management, sets session identification cookies on a different web application or manipulates the audience claims in tokens. This happens due to:

1. **Insufficient Domain and Path Restrictions:** The web application does not adequately restrict the domain and path for which its cookies are valid.
2. **Lack of Secure Cookie Attributes:** The application fails to use secure attributes (e.g., Secure, HttpOnly, SameSite) for its cookies, making them vulnerable to manipulation and cross-site attacks.
3. **Inadequate Token Audience Validation:** The application does not properly validate the audience claims in tokens, allowing them to be used across different applications or contexts.
4. **Absence of strong secret management:** The client is incapable of securly storing refresh tokens or cookies, making them vulnerable to theft and misuse.
5. **Absence of strong client authentication resistant to replay attacks:** The application does not implement strong client authentication methods, making it easier for attackers to impersonate legitimate users and misuse tokens or cookies.

### Example

Alison targets a web application that has loosely defined domain attributes for its cookies. She crafts a malicious script that, when executed on a user’s browser, sets a cookie intended for another domain. Due to the lack of strict domain and path restrictions, this cookie is accepted and used by the targeted web application. This allows Alison to track users or even hijack sessions across different applications or websites that don't securely restrict their cookie domains and paths.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Spoofing**.

**Spoofing** is about impersonating a legitimate user or entity.
Alison sets cookies for another web application due to insufficient domain/path restrictions, which lets her impersonate users or hijack their sessions on that application.
The root issue is unauthorized impersonation via session manipulation, making Spoofing the correct primary category.

### What can go wrong?

Such vulnerabilities can lead to cross-domain attacks, unauthorized session tracking, and potentially session hijacking, compromising user security on multiple applications.

There may be reasons to share sessions across multiple applications, but if one of those applications is less secure one application might be used to compromise another.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Ensure that session cookies are restricted to their intended domains to prevent cross-domain leakage.
2. Enforce HTTPS encryption for all website communication to prevent packet sniffing, and implement additional security measures like Secure and HttpOnly flags to protect cookies from being accessed by client-side scripts.
3. Use SameSite Cookie Attribute: Configure the SameSite attribute on cookies to prevent them from being sent with cross-site requests, which helps mitigate the risk of cross-site request forgery (CSRF).
4. Regularly change session IDs after authentication to minimize the impact of a compromised ID.
5. Regularly review and update cookie policies to align with best practices in web security.
6. Implement strong client authentication methods that are resistant to replay attacks, and ensure that authorization servers invalidate refresh tokens after use to prevent token theft.
7. Ensure that tokens are properly validated for their intended audience to prevent misuse across different applications.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
