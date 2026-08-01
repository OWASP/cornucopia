# Sanitization

## V1.3.1

Verify that all untrusted HTML input from WYSIWYG editors or similar is sanitized using a well-known and secure HTML sanitization library or framework feature.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [19](/taxonomy/capec-3.9/19), [231](/taxonomy/capec-3.9/231), [242](/taxonomy/capec-3.9/242), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28), [63](/taxonomy/capec-3.9/63)

## V1.3.2

Verify that the application avoids the use of eval() or other dynamic code execution features such as Spring Expression Language (SpEL). Where there is no alternative, any user input being included must be sanitized before being executed.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [184](/taxonomy/capec-3.9/184), [19](/taxonomy/capec-3.9/19), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [253](/taxonomy/capec-3.9/253), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [441](/taxonomy/capec-3.9/441), [523](/taxonomy/capec-3.9/523), [549](/taxonomy/capec-3.9/549), [586](/taxonomy/capec-3.9/586), [63](/taxonomy/capec-3.9/63)

## V1.3.3

Verify that data being passed to a potentially dangerous context is sanitized beforehand to enforce safety measures, such as only allowing characters which are safe for this context and trimming input which is too long.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126), [136](/taxonomy/capec-3.9/136), [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [184](/taxonomy/capec-3.9/184), [19](/taxonomy/capec-3.9/19), [231](/taxonomy/capec-3.9/231), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [253](/taxonomy/capec-3.9/253), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [43](/taxonomy/capec-3.9/43), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549), [63](/taxonomy/capec-3.9/63), [66](/taxonomy/capec-3.9/66), [676](/taxonomy/capec-3.9/676), [88](/taxonomy/capec-3.9/88)

## V1.3.4

Verify that user-supplied Scalable Vector Graphics (SVG) scriptable content is validated or sanitized to contain only tags and attributes (such as draw graphics) that are safe for the application, e.g., do not contain scripts and foreignObject.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [19](/taxonomy/capec-3.9/19), [23](/taxonomy/capec-3.9/23), [231](/taxonomy/capec-3.9/231), [242](/taxonomy/capec-3.9/242), [250](/taxonomy/capec-3.9/250), [253](/taxonomy/capec-3.9/253), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [63](/taxonomy/capec-3.9/63)

## V1.3.5

Verify that the application sanitizes or disables user-supplied scriptable or expression template language content, such as Markdown, CSS or XSL stylesheets, BBCode, or similar.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [19](/taxonomy/capec-3.9/19), [23](/taxonomy/capec-3.9/23), [231](/taxonomy/capec-3.9/231), [242](/taxonomy/capec-3.9/242), [250](/taxonomy/capec-3.9/250), [253](/taxonomy/capec-3.9/253), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [63](/taxonomy/capec-3.9/63)

## V1.3.6

Verify that the application protects against Server-side Request Forgery (SSRF) attacks, by validating untrusted data against an allowlist of protocols, domains, paths and ports and sanitizing potentially dangerous characters before using the data to call another service.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [184](/taxonomy/capec-3.9/184), [19](/taxonomy/capec-3.9/19), [201](/taxonomy/capec-3.9/201), [23](/taxonomy/capec-3.9/23), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [253](/taxonomy/capec-3.9/253), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [441](/taxonomy/capec-3.9/441), [51](/taxonomy/capec-3.9/51), [549](/taxonomy/capec-3.9/549), [63](/taxonomy/capec-3.9/63), [664](/taxonomy/capec-3.9/664)

## V1.3.7

Verify that the application protects against template injection attacks by not allowing templates to be built based on untrusted input. Where there is no alternative, any untrusted input being included dynamically during template creation must be sanitized or strictly validated.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [19](/taxonomy/capec-3.9/19), [23](/taxonomy/capec-3.9/23), [242](/taxonomy/capec-3.9/242), [250](/taxonomy/capec-3.9/250), [253](/taxonomy/capec-3.9/253), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [63](/taxonomy/capec-3.9/63)

## V1.3.8

Verify that the application appropriately sanitizes untrusted input before use in Java Naming and Directory Interface (JNDI) queries and that JNDI is configured securely to prevent JNDI injection attacks.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [176](/taxonomy/capec-3.9/176), [184](/taxonomy/capec-3.9/184), [201](/taxonomy/capec-3.9/201), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [253](/taxonomy/capec-3.9/253), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549), [586](/taxonomy/capec-3.9/586)

## V1.3.9

Verify that the application sanitizes content before it is sent to memcache to prevent injection attacks.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [141](/taxonomy/capec-3.9/141), [152](/taxonomy/capec-3.9/152), [242](/taxonomy/capec-3.9/242), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28)

## V1.3.10

Verify that format strings which might resolve in an unexpected or malicious way when used are sanitized before being processed.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [135](/taxonomy/capec-3.9/135), [137](/taxonomy/capec-3.9/137), [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [253](/taxonomy/capec-3.9/253), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549), [88](/taxonomy/capec-3.9/88)

## V1.3.11

Verify that the application sanitizes user input before passing to mail systems to protect against SMTP or IMAP injection.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [175](/taxonomy/capec-3.9/175), [183](/taxonomy/capec-3.9/183), [184](/taxonomy/capec-3.9/184), [19](/taxonomy/capec-3.9/19), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [253](/taxonomy/capec-3.9/253), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549)

## V1.3.12

Verify that regular expressions are free from elements causing exponential backtracking, and ensure untrusted input is sanitized to mitigate ReDoS or Runaway Regex attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [130](/taxonomy/capec-3.9/130), [152](/taxonomy/capec-3.9/152), [231](/taxonomy/capec-3.9/231), [242](/taxonomy/capec-3.9/242), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
