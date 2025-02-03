# Broken Access Controls
## Description
Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing a business function outside the user's limits. Common access control vulnerabilities include:

- Violation of the principle of least privilege or deny by default, where access should only be granted for particular capabilities, roles, or users, but is available to anyone.
- Bypassing access control checks by modifying the URL (parameter tampering or force browsing), internal application state, or the HTML page, or by using an attack tool modifying API requests.
- Permitting viewing or editing someone else's account, by providing its unique identifier (insecure direct object references)
- Accessing API with missing access controls for POST, PUT and DELETE.
- Elevation of privilege. Acting as a user without being logged in or acting as an admin when logged in as a user.
- Metadata manipulation, such as replaying or tampering with a JSON Web Token (JWT) access control token, or a cookie or hidden field manipulated to elevate privileges or abusing JWT invalidation.
- CORS misconfiguration allows API access from unauthorized/untrusted origins.
- Force browsing to authenticated pages as an unauthenticated user or to privileged pages as a standard user.

## How to Prevent
- Access control is only effective in trusted server-side code or server-less API, where the attacker cannot modify the access control check or metadata.
- Except for public resources, deny by default.
- Implement access control mechanisms once and re-use them throughout the application, including minimizing Cross-Origin Resource Sharing (CORS) usage.
- Model access controls should enforce record ownership rather than accepting that the user can create, read, update, or delete any record.
- Unique application business limit requirements should be enforced by domain models.
- Disable web server directory listing and ensure file metadata (e.g., .git) and backup files are not present within web roots.
- Log access control failures, alert admins when appropriate (e.g., repeated failures).
- Rate limit API and controller access to minimize the harm from automated attack tooling.
- Stateful session identifiers should be invalidated on the server after logout. Stateless JWT tokens should rather be short-lived so that the window of opportunity for an attacker is minimized. For longer lived JWTs it's highly recommended to follow the OAuth standards to revoke access.
- Developers and QA staff should include functional access control unit and integration tests.

[Source: OWASP TOP 10 broken access controls](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

## Cheatsheets
[Broken Access Controls Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a012021-broken-access-control)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)
- [Data-validation-&-encoding 6](/data-validation-&-encoding/6)
- [Data-validation-&-encoding 7](/data-validation-&-encoding/7)
- [Data-validation-&-encoding 8](/data-validation-&-encoding/8)
- [Data-validation-&-encoding 9](/data-validation-&-encoding/9)
- [Data-validation-&-encoding 10](/data-validation-&-encoding/10)
- [Data-validation-&-encoding J](/data-validation-&-encoding/J)
- [Data-validation-&-encoding K](/data-validation-&-encoding/K)

### Authentication
- [Authentication 2](/authentication/2)
- [Authentication 8](/authentication/8)
- [Authentication 9](/authentication/9)
- [Authentication 10](/authentication/10)
- [Authentication Q](/authentication/Q)
- [Authentication K](/authentication/K)

### Authorization
- [Authorization 3](/authorization/3)
- [Authorization 4](/authorization/4)
- [Authorization 5](/authorization/5)
- [Authorization 6](/authorization/6)
- [Authorization 7](/authorization/7)
- [Authorization 8](/authorization/8)
- [Authorization 10](/authorization/10)
- [Authorization J](/authorization/J)
- [Authorization K](/authorization/K)

### Cryptography
- [Cryptography 8](/cryptography/8)
- [Cryptography 10](/cryptography/10)
- [Cryptography K](/cryptography/K)

### Cornucopia
- [Cornucopia 2](/cornucopia/2)
- [Cornucopia K](/cornucopia/K)
