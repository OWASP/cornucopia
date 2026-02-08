# File Download

## V5.4.1

Verify that the application validates or ignores user-submitted filenames, including in a JSON, JSONP, or URL parameter and specifies a filename in the Content-Disposition header field in the response.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126/index.md), [137](/taxonomy/capec-3.9/137/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [165](/taxonomy/capec-3.9/165/index.md), [175](/taxonomy/capec-3.9/175/index.md), [184](/taxonomy/capec-3.9/184/index.md), [23](/taxonomy/capec-3.9/23/index.md), [242](/taxonomy/capec-3.9/242/index.md), [248](/taxonomy/capec-3.9/248/index.md), [272](/taxonomy/capec-3.9/272/index.md), [441](/taxonomy/capec-3.9/441/index.md), [444](/taxonomy/capec-3.9/444/index.md), [48](/taxonomy/capec-3.9/48/index.md), [523](/taxonomy/capec-3.9/523/index.md), [549](/taxonomy/capec-3.9/549/index.md), [586](/taxonomy/capec-3.9/586/index.md), [636](/taxonomy/capec-3.9/636/index.md), [64](/taxonomy/capec-3.9/64/index.md), [66](/taxonomy/capec-3.9/66/index.md)

## V5.4.2

Verify that file names served (e.g., in HTTP response header fields or email attachments) are encoded or sanitized (e.g., following RFC 6266) to preserve document structure and prevent injection attacks.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126/index.md), [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [165](/taxonomy/capec-3.9/165/index.md), [175](/taxonomy/capec-3.9/175/index.md), [184](/taxonomy/capec-3.9/184/index.md), [23](/taxonomy/capec-3.9/23/index.md), [242](/taxonomy/capec-3.9/242/index.md), [248](/taxonomy/capec-3.9/248/index.md), [267](/taxonomy/capec-3.9/267/index.md), [28](/taxonomy/capec-3.9/28/index.md), [43](/taxonomy/capec-3.9/43/index.md), [441](/taxonomy/capec-3.9/441/index.md), [444](/taxonomy/capec-3.9/444/index.md), [48](/taxonomy/capec-3.9/48/index.md), [52](/taxonomy/capec-3.9/52/index.md), [523](/taxonomy/capec-3.9/523/index.md), [549](/taxonomy/capec-3.9/549/index.md), [586](/taxonomy/capec-3.9/586/index.md), [636](/taxonomy/capec-3.9/636/index.md), [64](/taxonomy/capec-3.9/64/index.md), [66](/taxonomy/capec-3.9/66/index.md)

## V5.4.3

Verify that files obtained from untrusted sources are scanned by antivirus scanners to prevent serving of known malicious content.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [122](/taxonomy/capec-3.9/122/index.md), [126](/taxonomy/capec-3.9/126/index.md), [175](/taxonomy/capec-3.9/175/index.md), [184](/taxonomy/capec-3.9/184/index.md), [23](/taxonomy/capec-3.9/23/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [248](/taxonomy/capec-3.9/248/index.md), [253](/taxonomy/capec-3.9/253/index.md), [441](/taxonomy/capec-3.9/441/index.md), [444](/taxonomy/capec-3.9/444/index.md), [523](/taxonomy/capec-3.9/523/index.md), [549](/taxonomy/capec-3.9/549/index.md), [636](/taxonomy/capec-3.9/636/index.md), [66](/taxonomy/capec-3.9/66/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
