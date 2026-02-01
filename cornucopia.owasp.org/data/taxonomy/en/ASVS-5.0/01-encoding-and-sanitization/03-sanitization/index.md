# Sanitization
## V1.3.1
Verify that all untrusted HTML input from WYSIWYG editors or similar is sanitized using a well-known and secure HTML sanitization library or framework feature.
Required for Level 1, 2 and 3
## V1.3.2
Verify that the application avoids the use of eval() or other dynamic code execution features such as Spring Expression Language (SpEL). Where there is no alternative, any user input being included must be sanitized before being executed.
Required for Level 1, 2 and 3
## V1.3.3
Verify that data being passed to a potentially dangerous context is sanitized beforehand to enforce safety measures, such as only allowing characters which are safe for this context and trimming input which is too long.
Required for Level 2 and 3
## V1.3.4
Verify that user-supplied Scalable Vector Graphics (SVG) scriptable content is validated or sanitized to contain only tags and attributes (such as draw graphics) that are safe for the application, e.g., do not contain scripts and foreignObject.
Required for Level 2 and 3
## V1.3.5
Verify that the application sanitizes or disables user-supplied scriptable or expression template language content, such as Markdown, CSS or XSL stylesheets, BBCode, or similar.
Required for Level 2 and 3
## V1.3.6
Verify that the application protects against Server-side Request Forgery (SSRF) attacks, by validating untrusted data against an allowlist of protocols, domains, paths and ports and sanitizing potentially dangerous characters before using the data to call another service.
Required for Level 2 and 3
## V1.3.7
Verify that the application protects against template injection attacks by not allowing templates to be built based on untrusted input. Where there is no alternative, any untrusted input being included dynamically during template creation must be sanitized or strictly validated.
Required for Level 2 and 3
## V1.3.8
Verify that the application appropriately sanitizes untrusted input before use in Java Naming and Directory Interface (JNDI) queries and that JNDI is configured securely to prevent JNDI injection attacks.
Required for Level 2 and 3
## V1.3.9
Verify that the application sanitizes content before it is sent to memcache to prevent injection attacks.
Required for Level 2 and 3
## V1.3.10
Verify that format strings which might resolve in an unexpected or malicious way when used are sanitized before being processed.
Required for Level 2 and 3
## V1.3.11
Verify that the application sanitizes user input before passing to mail systems to protect against SMTP or IMAP injection.
Required for Level 2 and 3
## V1.3.12
Verify that regular expressions are free from elements causing exponential backtracking, and ensure untrusted input is sanitized to mitigate ReDoS or Runaway Regex attacks.
Required for Level 3
## Disclaimer
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
