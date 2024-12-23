#  Sanitization and Sandboxing
## V5.2.1
Verify that all untrusted HTML input from WYSIWYG editors or similar is properly sanitized with an HTML sanitizer library or framework feature. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [116](https://cwe.mitre.org/data/definitions/116)
## V5.2.2
Verify that unstructured data is sanitized to enforce safety measures such as allowed characters and length.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [138](https://cwe.mitre.org/data/definitions/138)
## V5.2.3
Verify that the application sanitizes user input before passing to mail systems to protect against SMTP or IMAP injection.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [147](https://cwe.mitre.org/data/definitions/147)
## V5.2.4
Verify that the application avoids the use of eval() or other dynamic code execution features. Where there is no alternative, any user input being included must be sanitized or sandboxed before being executed.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [95](https://cwe.mitre.org/data/definitions/95)
## V5.2.5
Verify that the application protects against template injection attacks by ensuring that any user input being included is sanitized or sandboxed.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [94](https://cwe.mitre.org/data/definitions/94)
## V5.2.6
Verify that the application protects against SSRF attacks, by validating or sanitizing untrusted data or HTTP file metadata, such as filenames and URL input fields, and uses allow lists of protocols, domains, paths and ports.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [918](https://cwe.mitre.org/data/definitions/918)
## V5.2.7
Verify that the application sanitizes, disables, or sandboxes user-supplied Scalable Vector Graphics (SVG) scriptable content, especially as they relate to XSS resulting from inline scripts, and foreignObject.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [159](https://cwe.mitre.org/data/definitions/159)
## V5.2.8
Verify that the application sanitizes, disables, or sandboxes user-supplied scriptable or expression template language content, such as Markdown, CSS or XSL stylesheets, BBCode, or similar.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [94](https://cwe.mitre.org/data/definitions/94)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
