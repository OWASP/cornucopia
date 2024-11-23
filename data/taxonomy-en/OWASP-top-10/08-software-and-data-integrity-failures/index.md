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
- [Data-validation-&-encoding 2](/data-validation-&-encoding/VE2)
- [Data-validation-&-encoding 3](/data-validation-&-encoding/VE3)
- [Data-validation-&-encoding 5](/data-validation-&-encoding/VE5)
- [Data-validation-&-encoding 6](/data-validation-&-encoding/VE6)
- [Data-validation-&-encoding 7](/data-validation-&-encoding/VE7)
- [Data-validation-&-encoding 8](/data-validation-&-encoding/VE8)
- [Data-validation-&-encoding 9](/data-validation-&-encoding/VE9)
- [Data-validation-&-encoding 10](/data-validation-&-encoding/VEX)
- [Data-validation-&-encoding J](/data-validation-&-encoding/VEJ)
- [Data-validation-&-encoding Q](/data-validation-&-encoding/VEQ)
- [Data-validation-&-encoding K](/data-validation-&-encoding/VEK)

### Authentication
- [Authentication 2](/authentication/AT2)
- [Authentication 3](/authentication/AT3)
- [Authentication 4](/authentication/AT4)
- [Authentication 5](/authentication/AT5)
- [Authentication 6](/authentication/AT6)
- [Authentication 7](/authentication/AT7)
- [Authentication 9](/authentication/AT9)
- [Authentication 10](/authentication/ATX)
- [Authentication J](/authentication/ATJ)
- [Authentication Q](/authentication/ATQ)
- [Authentication K](/authentication/ATK)

### Session-management
- [Session-management 2](/session-management/SM2)
- [Session-management 4](/session-management/SM4)
- [Session-management 5](/session-management/SM5)
- [Session-management 6](/session-management/SM6)
- [Session-management 7](/session-management/SM7)
- [Session-management 8](/session-management/SM8)
- [Session-management 9](/session-management/SM9)
- [Session-management 10](/session-management/SMX)
- [Session-management J](/session-management/SMJ)
- [Session-management Q](/session-management/SMQ)
- [Session-management K](/session-management/SMK)

### Authorization
- [Authorization 3](/authorization/AZ3)
- [Authorization 5](/authorization/AZ5)
- [Authorization 8](/authorization/AZ8)
- [Authorization 9](/authorization/AZ9)

### Cryptography
- [Cryptography 3](/cryptography/CR3)
- [Cryptography J](/cryptography/CRJ)

### Cornucopia
- [Cornucopia 2](/cornucopia/C2)
- [Cornucopia 3](/cornucopia/C3)
- [Cornucopia 6](/cornucopia/C6)
- [Cornucopia 7](/cornucopia/C7)
- [Cornucopia 10](/cornucopia/CX)
- [Cornucopia J](/cornucopia/CJ)
- [Cornucopia K](/cornucopia/CK)
