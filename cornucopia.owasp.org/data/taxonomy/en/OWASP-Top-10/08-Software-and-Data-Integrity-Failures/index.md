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
- [Data-validation-&-encoding 2](/cards/VE2)
- [Data-validation-&-encoding 3](/cards/VE3)
- [Data-validation-&-encoding 5](/cards/VE5)
- [Data-validation-&-encoding 6](/cards/VE6)
- [Data-validation-&-encoding 7](/cards/VE7)
- [Data-validation-&-encoding 8](/cards/VE8)
- [Data-validation-&-encoding 9](/cards/VE9)
- [Data-validation-&-encoding 10](/cards/VEX)
- [Data-validation-&-encoding J](/cards/VEJ)
- [Data-validation-&-encoding Q](/cards/VEQ)
- [Data-validation-&-encoding K](/cards/VEK)

### Authentication
- [Authentication 2](/cards/AT2)
- [Authentication 3](/cards/AT3)
- [Authentication 4](/cards/AT4)
- [Authentication 5](/cards/AT5)
- [Authentication 6](/cards/AT6)
- [Authentication 7](/cards/AT7)
- [Authentication 9](/cards/AT9)
- [Authentication 10](/cards/ATX)
- [Authentication J](/cards/ATJ)
- [Authentication Q](/cards/ATQ)
- [Authentication K](/cards/ATK)

### Session-management
- [Session-management 2](/cards/SM2)
- [Session-management 4](/cards/SM4)
- [Session-management 5](/cards/SM5)
- [Session-management 6](/cards/SM6)
- [Session-management 7](/cards/SM7)
- [Session-management 8](/cards/SM8)
- [Session-management 9](/cards/SM9)
- [Session-management 10](/cards/SMX)
- [Session-management J](/cards/SMJ)
- [Session-management Q](/cards/SMQ)
- [Session-management K](/cards/SMK)

### Authorization
- [Authorization 3](/cards/AZ3)
- [Authorization 5](/cards/AZ5)
- [Authorization 8](/cards/AZ8)
- [Authorization 9](/cards/AZ9)

### Cryptography
- [Cryptography 3](/cards/CR3)
- [Cryptography J](/cards/CRJ)

### Cornucopia
- [Cornucopia 2](/cards/C2)
- [Cornucopia 3](/cards/C3)
- [Cornucopia 6](/cards/C6)
- [Cornucopia 7](/cards/C7)
- [Cornucopia 10](/cards/CX)
- [Cornucopia J](/cards/CJ)
- [Cornucopia K](/cards/CK)
