# Software and Data Integrity Failures 
## Description
Software and data integrity failures relate to code and infrastructure that does not protect against integrity violations. An example of this is where an application relies upon plugins, libraries, or modules from untrusted sources, repositories, and content delivery networks (CDNs). An insecure CI/CD pipeline can introduce the potential for unauthorized access, malicious code, or system compromise. Lastly, many applications now include auto-update functionality, where updates are downloaded without sufficient integrity verification and applied to the previously trusted application. Attackers could potentially upload their own updates to be distributed and run on all installations. Another example is where objects or data are encoded or serialized into a structure that an attacker can see and modify is vulnerable to insecure deserialization.

## How to Prevent
- Use digital signatures or similar mechanisms to verify the software or data is from the expected source and has not been altered.
- Ensure libraries and dependencies, such as npm or Maven, are consuming trusted repositories. If you have a higher risk profile, consider hosting an internal known-good repository that's vetted.
- Ensure that a software supply chain security tool, such as OWASP Dependency Check or OWASP CycloneDX, is used to verify that components do not contain known vulnerabilities
- Ensure that there is a review process for code and configuration changes to minimize the chance that malicious code or configuration could be introduced into your software pipeline.
- Ensure that your CI/CD pipeline has proper segregation, configuration, and access control to ensure the integrity of the code flowing through the build and deploy processes.
- Ensure that unsigned or unencrypted serialized data is not sent to untrusted clients without some form of integrity check or digital signature to detect tampering or replay of the serialized data

[Source: OWASP TOP 10 Software and Data Integrity Failures ](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)

## Cheatsheets
[Software and Data Integrity Failures Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a082021-software-and-data-integrity-failures)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)
- [Data-validation-&-encoding 3](/data-validation-&-encoding/3)
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
- [Authentication 6](/authentication/6)
- [Authentication 7](/authentication/7)
- [Authentication 9](/authentication/9)
- [Authentication 10](/authentication/10)
- [Authentication J](/authentication/J)
- [Authentication Q](/authentication/Q)
- [Authentication K](/authentication/K)

### Session-management
- [Session-management 2](/session-management/2)
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
- [Authorization 5](/authorization/5)
- [Authorization 8](/authorization/8)
- [Authorization 9](/authorization/9)

### Cryptography
- [Cryptography 3](/cryptography/3)
- [Cryptography J](/cryptography/J)

### Cornucopia
- [Cornucopia 2](/cornucopia/2)
- [Cornucopia 3](/cornucopia/3)
- [Cornucopia 6](/cornucopia/6)
- [Cornucopia 7](/cornucopia/7)
- [Cornucopia 10](/cornucopia/10)
- [Cornucopia J](/cornucopia/J)
- [Cornucopia K](/cornucopia/K)
