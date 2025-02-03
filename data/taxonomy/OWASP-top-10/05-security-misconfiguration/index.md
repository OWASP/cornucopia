# Security Misconfiguration
## Description
The application might be vulnerable if the application is:

- Missing appropriate security hardening across any part of the application stack or improperly configured permissions on cloud services.
- Unnecessary features are enabled or installed (e.g., unnecessary ports, services, pages, accounts, or privileges).
- Default accounts and their passwords are still enabled and unchanged.
- Error handling reveals stack traces or other overly informative error messages to users.
- For upgraded systems, the latest security features are disabled or not configured securely.
- The security settings in the application servers, application frameworks (e.g., Struts, Spring, ASP.NET), libraries, databases, etc., are not set to secure values.
- The server does not send security headers or directives, or they are not set to secure values.
- The software is out of date or vulnerable (see A06:2021-Vulnerable and Outdated Components).

Without a concerted, repeatable application security configuration process, systems are at a higher risk.

## How to Prevent
- A repeatable hardening process makes it fast and easy to deploy another environment that is appropriately locked down. Development, QA, and production environments should all be configured identically, with different credentials used in each environment. This process should be automated to minimize the effort required to set up a new secure environment.
- A minimal platform without any unnecessary features, components, documentation, and samples. Remove or do not install unused features and frameworks.
- A task to review and update the configurations appropriate to all security notes, updates, and patches as part of the patch management process (see A06:2021-Vulnerable and Outdated Components). Review cloud storage permissions (e.g., S3 bucket permissions).
- A segmented application architecture provides effective and secure separation between components or tenants, with segmentation, containerization, or cloud security groups (ACLs).
- Sending security directives to clients, e.g., Security Headers.
- An automated process to verify the effectiveness of the configurations and settings in all environments.

[Source: OWASP TOP 10 Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)

## Cheatsheets
[Security Misconfiguration Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a052021-security-misconfiguration)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)
- [Data-validation-&-encoding 3](/data-validation-&-encoding/3)
- [Data-validation-&-encoding 4](/data-validation-&-encoding/4)
- [Data-validation-&-encoding 5](/data-validation-&-encoding/5)
- [Data-validation-&-encoding 6](/data-validation-&-encoding/6)
- [Data-validation-&-encoding 7](/data-validation-&-encoding/7)
- [Data-validation-&-encoding 8](/data-validation-&-encoding/8)
- [Data-validation-&-encoding 9](/data-validation-&-encoding/9)
- [Data-validation-&-encoding 10](/data-validation-&-encoding/10)
- [Data-validation-&-encoding J](/data-validation-&-encoding/J)
- [Data-validation-&-encoding Q](/data-validation-&-encoding/Q)
- [Data-validation-&-encoding K](/data-validation-&-encoding/K)

### Authentication
- [Authentication 2](/authentication/2)
- [Authentication 3](/authentication/3)
- [Authentication 4](/authentication/4)
- [Authentication 5](/authentication/5)
- [Authentication 8](/authentication/8)
- [Authentication 9](/authentication/9)
- [Authentication 10](/authentication/10)
- [Authentication J](/authentication/J)
- [Authentication Q](/authentication/Q)

### Session-management
- [Session-management 2](/session-management/2)
- [Session-management 3](/session-management/3)
- [Session-management 4](/session-management/4)
- [Session-management 5](/session-management/5)
- [Session-management 6](/session-management/6)
- [Session-management 7](/session-management/7)
- [Session-management 8](/session-management/8)
- [Session-management 9](/session-management/9)
- [Session-management 10](/session-management/10)
- [Session-management J](/session-management/J)
- [Session-management Q](/session-management/Q)
- [Session-management K](/session-management/K)

### Authorization
- [Authorization 3](/authorization/3)
- [Authorization 4](/authorization/4)
- [Authorization 8](/authorization/8)
- [Authorization 9](/authorization/9)
- [Authorization J](/authorization/J)

### Cornucopia
- [Cornucopia 2](/cornucopia/2)
- [Cornucopia 3](/cornucopia/3)
- [Cornucopia 6](/cornucopia/6)
- [Cornucopia 8](/cornucopia/8)
- [Cornucopia 9](/cornucopia/9)
- [Cornucopia J](/cornucopia/J)
- [Cornucopia K](/cornucopia/K)
