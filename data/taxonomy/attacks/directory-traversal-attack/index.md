# Directory Traversal Attack
Directory Traversal Attack, also known as path traversal or ../ (dot dot slash) attack, is a security exploit where an attacker can access directories and files that are stored outside the web root folder. This type of attack occurs when a web application does not properly validate or sanitize user input, allowing an attacker to navigate the file system.

## Example
The Cisco Duo Device Health Application for Windows has a vulnerability allowing a low-privileged attacker to perform directory traversal attacks, potentially overwriting files on the device. Directory traversal enables unauthorized access to restricted directories. Cisco has released software upgrades to fix the issue, emphasizing its high severity (CVSS score of 7.1). The vulnerability results from insufficient input validation, and successful exploitation could lead to overwriting files with SYSTEM-level privileges, causing potential DoS or data loss.

## Links
- [Cisco Directory Traversal Attacks](https://cybersecuritynews.com/cisco-duo-device-health-app-flaw/)
- [Path Traversal | OWASP Foundation](https://owasp.org/www-community/attacks/Path_Traversal)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)
