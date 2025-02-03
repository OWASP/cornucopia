# Insecure Session Storage
Insecure Session Storage refers to the unsafe use of session storage in web development, where sensitive data is stored without proper security measures. This can lead to vulnerabilities such as cross-site scripting and unauthorized access to confidential information.

## Example
In a fictional scenario, an attacker named Eve exploits an online banking application's insecure use of ‘sessionStorage’ to conduct a session hijacking attack. Discovering the vulnerability, Eve injects a script that captures users' session tokens and sends them to her server. When a user like Alice logs in, Eve intercepts the session token, allowing her unauthorized access to the victim's account. In this case, Eve impersonates Alice, initiates unauthorized transactions, and causes financial harm.

## Links
- [Insecure Data Storage | OWASP Foundation](https://owasp.org/www-project-mobile-top-10/2023-risks/m9-insecure-data-storage)
- [IDOR - Inside the Session Storage](https://shahjerry33.medium.com/idor-inside-the-session-storage-88af485fc899)

## Cards
### Authentication
- [Authentication 3](/authentication/3)
