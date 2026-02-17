# Injection Prevention

## V1.2.1

Verify that output encoding for an HTTP response, HTML document, or XML document is relevant for the context required, such as encoding the relevant characters for HTML elements, HTML attributes, HTML comments, CSS, or HTTP header fields, to avoid changing the message or document structure.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [160](/taxonomy/capec-3.9/160), [19](/taxonomy/capec-3.9/19), [242](/taxonomy/capec-3.9/242), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28), [43](/taxonomy/capec-3.9/43), [63](/taxonomy/capec-3.9/63)

## V1.2.2

Verify that when dynamically building URLs, untrusted data is encoded according to its context (e.g., URL encoding or base64url encoding for query or path parameters). Ensure that only safe URL protocols are permitted (e.g., disallow javascript: or data:).

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [137](/taxonomy/capec-3.9/137), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [160](/taxonomy/capec-3.9/160), [19](/taxonomy/capec-3.9/19), [242](/taxonomy/capec-3.9/242), [267](/taxonomy/capec-3.9/267), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [43](/taxonomy/capec-3.9/43), [586](/taxonomy/capec-3.9/586), [63](/taxonomy/capec-3.9/63), [64](/taxonomy/capec-3.9/64), [72](/taxonomy/capec-3.9/72)

## V1.2.3

Verify that output encoding or escaping is used when dynamically building JavaScript content (including JSON), to avoid changing the message or document structure (to avoid JavaScript and JSON injection).

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [122](/taxonomy/capec-3.9/122), [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [19](/taxonomy/capec-3.9/19), [233](/taxonomy/capec-3.9/233), [242](/taxonomy/capec-3.9/242), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28), [43](/taxonomy/capec-3.9/43), [63](/taxonomy/capec-3.9/63), [636](/taxonomy/capec-3.9/636), [93](/taxonomy/capec-3.9/93)

## V1.2.4

Verify that data selection or database queries (e.g., SQL, HQL, NoSQL, Cypher) use parameterized queries, ORMs, entity frameworks, or are otherwise protected from SQL Injection and other database injection attacks. This is also relevant when writing stored procedures.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [153](/taxonomy/capec-3.9/153), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549), [66](/taxonomy/capec-3.9/66), [676](/taxonomy/capec-3.9/676), [93](/taxonomy/capec-3.9/93)

## V1.2.5

Verify that the application protects against OS command injection and that operating system calls use parameterized OS queries or use contextual command line output encoding.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [153](/taxonomy/capec-3.9/153), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549), [88](/taxonomy/capec-3.9/88)

## V1.2.6

Verify that the application protects against LDAP injection vulnerabilities, or that specific security controls to prevent LDAP injection have been implemented.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [136](/taxonomy/capec-3.9/136), [153](/taxonomy/capec-3.9/153), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549)

## V1.2.7

Verify that the application is protected against XPath injection attacks by using query parameterization or precompiled queries.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [153](/taxonomy/capec-3.9/153), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [250](/taxonomy/capec-3.9/250), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549), [83](/taxonomy/capec-3.9/83)

## V1.2.8

Verify that LaTeX processors are configured securely (such as not using the "--shell-escape" flag) and an allowlist of commands is used to prevent LaTeX injection attacks.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [153](/taxonomy/capec-3.9/153), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549)

## V1.2.9

Verify that the application escapes special characters in regular expressions (typically using a backslash) to prevent them from being misinterpreted as metacharacters.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [120](/taxonomy/capec-3.9/120), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [28](/taxonomy/capec-3.9/28), [3](/taxonomy/capec-3.9/3), [4](/taxonomy/capec-3.9/4), [43](/taxonomy/capec-3.9/43), [441](/taxonomy/capec-3.9/441), [549](/taxonomy/capec-3.9/549), [64](/taxonomy/capec-3.9/64), [71](/taxonomy/capec-3.9/71), [72](/taxonomy/capec-3.9/72), [78](/taxonomy/capec-3.9/78), [79](/taxonomy/capec-3.9/79), [80](/taxonomy/capec-3.9/80)

## V1.2.10

Verify that the application is protected against CSV and Formula Injection. The application must follow the escaping rules defined in RFC 4180 sections 2.6 and 2.7 when exporting CSV content. Additionally, when exporting to CSV or other spreadsheet formats (such as XLS, XLSX, or ODF), special characters (including '=', '+', '-', '@', '\t' (tab), and '\0' (null character)) must be escaped with a single quote if they appear as the first character in a field value.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [153](/taxonomy/capec-3.9/153), [184](/taxonomy/capec-3.9/184), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [28](/taxonomy/capec-3.9/28), [3](/taxonomy/capec-3.9/3), [43](/taxonomy/capec-3.9/43), [441](/taxonomy/capec-3.9/441), [52](/taxonomy/capec-3.9/52), [549](/taxonomy/capec-3.9/549)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
