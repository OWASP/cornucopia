#  File Download
## V12.5.1
Verify that the web tier is configured to serve only files with specific file extensions to prevent unintentional information and source code leakage. For example, backup files (e.g. .bak), temporary working files (e.g. .swp), compressed files (.zip, .tar.gz, etc) and other extensions commonly used by editors should be blocked unless required.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [552](https://cwe.mitre.org/data/definitions/552)
## V12.5.2
Verify that direct requests to uploaded files will never be executed as HTML/JavaScript content.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [434](https://cwe.mitre.org/data/definitions/434)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
