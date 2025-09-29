## Scenario: Alison’s Cookie Manipulation Across Domains

Visualize a situation where Alison, exploiting weaknesses in cookie management, sets session identification cookies on a different web application. This happens due to:

1. **Insufficient Domain and Path Restrictions:** The web application does not adequately restrict the domain and path for which its cookies are valid.

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

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Strictly define and enforce domain and path attributes for all cookies, especially those used for session management, to ensure they are only sent to the appropriate domains and paths.
2. Implement additional security measures like Secure and HttpOnly flags to protect cookies from being accessed by client-side scripts.
3. Regularly review and update cookie policies to align with best practices in web security.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
