# File Upload and Content

## V5.2.1

Verify that the application will only accept files of a size which it can process without causing a loss of performance or a denial of service attack.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126/index.md), [130](/taxonomy/capec-3.9/130/index.md), [165](/taxonomy/capec-3.9/165/index.md), [572](/taxonomy/capec-3.9/572/index.md)

## V5.2.2

Verify that when the application accepts a file, either on its own or within an archive such as a zip file, it checks if the file extension matches an expected file extension and validates that the contents correspond to the type represented by the extension. This includes, but is not limited to, checking the initial 'magic bytes', performing image re-writing, and using specialized libraries for file content validation. For L1, this can focus just on files which are used to make specific business or security decisions. For L2 and up, this must apply to all files being accepted.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126/index.md), [165](/taxonomy/capec-3.9/165/index.md), [175](/taxonomy/capec-3.9/175/index.md), [184](/taxonomy/capec-3.9/184/index.md), [23](/taxonomy/capec-3.9/23/index.md), [242](/taxonomy/capec-3.9/242/index.md), [248](/taxonomy/capec-3.9/248/index.md), [253](/taxonomy/capec-3.9/253/index.md), [441](/taxonomy/capec-3.9/441/index.md), [444](/taxonomy/capec-3.9/444/index.md), [523](/taxonomy/capec-3.9/523/index.md), [549](/taxonomy/capec-3.9/549/index.md), [636](/taxonomy/capec-3.9/636/index.md), [66](/taxonomy/capec-3.9/66/index.md)

## V5.2.3

Verify that the application checks compressed files (e.g., zip, gz, docx, odt) against maximum allowed uncompressed size and against maximum number of files before uncompressing the file.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126/index.md), [165](/taxonomy/capec-3.9/165/index.md), [23](/taxonomy/capec-3.9/23/index.md), [66](/taxonomy/capec-3.9/66/index.md)

## V5.2.4

Verify that a file size quota and maximum number of files per user are enforced to ensure that a single user cannot fill up the storage with too many files, or excessively large files.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [165](/taxonomy/capec-3.9/165/index.md)

## V5.2.5

Verify that the application does not allow uploading compressed files containing symlinks unless this is specifically required (in which case it will be necessary to enforce an allowlist of the files that can be symlinked to).

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126/index.md), [153](/taxonomy/capec-3.9/153/index.md), [165](/taxonomy/capec-3.9/165/index.md), [23](/taxonomy/capec-3.9/23/index.md), [66](/taxonomy/capec-3.9/66/index.md)

## V5.2.6

Verify that the application rejects uploaded images with a pixel size larger than the maximum allowed, to prevent pixel flood attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [130](/taxonomy/capec-3.9/130/index.md), [165](/taxonomy/capec-3.9/165/index.md), [572](/taxonomy/capec-3.9/572/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
