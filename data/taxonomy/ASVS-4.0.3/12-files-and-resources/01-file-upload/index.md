#  File Upload
## V12.1.1
Verify that the application will not accept large files that could fill up storage or cause a denial of service.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [400](https://cwe.mitre.org/data/definitions/400)
## V12.1.2
Verify that the application checks compressed files (e.g. zip, gz, docx, odt) against maximum allowed uncompressed size and against maximum number of files before uncompressing the file.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [409](https://cwe.mitre.org/data/definitions/409)
## V12.1.3
Verify that a file size quota and maximum number of files per user is enforced to ensure that a single user cannot fill up the storage with too many files, or excessively large files.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [770](https://cwe.mitre.org/data/definitions/770)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
