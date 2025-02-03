# Server-Side Request Forgery (SSRF)
## Description
SSRF flaws occur whenever a web application is fetching a remote resource without validating the user-supplied URL. It allows an attacker to coerce the application to send a crafted request to an unexpected destination, even when protected by a firewall, VPN, or another type of network access control list (ACL).

As modern web applications provide end-users with convenient features, fetching a URL becomes a common scenario. As a result, the incidence of SSRF is increasing. Also, the severity of SSRF is becoming higher due to cloud services and the complexity of architectures.

## How to Prevent
Developers can prevent SSRF by implementing some or all the following defense in depth controls:

**From Network layer:**
- Segment remote resource access functionality in separate networks to reduce the impact of SSRF
- Enforce “deny by default” firewall policies or network access control rules to block all but essential intranet traffic.
Hints:
~ Establish an ownership and a lifecycle for firewall rules based on applications.
~ Log all accepted and blocked network flows on firewalls (see A09:2021-Security Logging and Monitoring Failures).

**From Application layer:**
- Sanitize and validate all client-supplied input data
- Enforce the URL schema, port, and destination with a positive allow list
- Do not send raw responses to clients
- Disable HTTP redirections
- Be aware of the URL consistency to avoid attacks such as DNS rebinding and “time of check, time of use” (TOCTOU) race conditions

Do not mitigate SSRF via the use of a deny list or regular expression. Attackers have payload lists, tools, and skills to bypass deny lists.

**Additional Measures to consider:**
- Don't deploy other security relevant services on front systems (e.g. OpenID). Control local traffic on these systems (e.g. localhost)
- For frontends with dedicated and manageable user groups use network encryption (e.g. VPNs) on independent systems to consider very high protection needs

[Source: OWASP TOP 10 Server-Side Request Forgery (SSRF)](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)

## Cheatsheets
[Server-Side Request Forgery (SSRF) Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a102021-server-side-request-forgery-ssrf)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)
- [Data-validation-&-encoding 7](/data-validation-&-encoding/7)
- [Data-validation-&-encoding Q](/data-validation-&-encoding/Q)

### Session-management
- [Session-management 4](/session-management/4)
- [Session-management 10](/session-management/10)

### Authorization
- [Authorization 2](/authorization/2)
- [Authorization 8](/authorization/8)
- [Authorization 9](/authorization/9)

### Cryptography
- [Cryptography 7](/cryptography/7)
- [Cryptography J](/cryptography/J)

### Cornucopia
- [Cornucopia 3](/cornucopia/3)
- [Cornucopia 5](/cornucopia/5)
- [Cornucopia Q](/cornucopia/Q)