# Insecure Design
## Description
Insecure design is a broad category representing different weaknesses, expressed as “missing or ineffective control design.” Insecure design is not the source for all other Top 10 risk categories. There is a difference between insecure design and insecure implementation. We differentiate between design flaws and implementation defects for a reason, they have different root causes and remediation. A secure design can still have implementation defects leading to vulnerabilities that may be exploited. An insecure design cannot be fixed by a perfect implementation as by definition, needed security controls were never created to defend against specific attacks. One of the factors that contribute to insecure design is the lack of business risk profiling inherent in the software or system being developed, and thus the failure to determine what level of security design is required.

**Requirements and Resource Management**

Collect and negotiate the business requirements for an application with the business, including the protection requirements concerning confidentiality, integrity, availability, and authenticity of all data assets and the expected business logic. Take into account how exposed your application will be and if you need segregation of tenants (additionally to access control). Compile the technical requirements, including functional and non-functional security requirements. Plan and negotiate the budget covering all design, build, testing, and operation, including security activities.

**Secure Design**

Secure design is a culture and methodology that constantly evaluates threats and ensures that code is robustly designed and tested to prevent known attack methods. Threat modeling should be integrated into refinement sessions (or similar activities); look for changes in data flows and access control or other security controls. In the user story development determine the correct flow and failure states, ensure they are well understood and agreed upon by responsible and impacted parties. Analyze assumptions and conditions for expected and failure flows, ensure they are still accurate and desirable. Determine how to validate the assumptions and enforce conditions needed for proper behaviors. Ensure the results are documented in the user story. Learn from mistakes and offer positive incentives to promote improvements. Secure design is neither an add-on nor a tool that you can add to software.

**Secure Development Lifecycle**

Secure software requires a secure development lifecycle, some form of secure design pattern, paved road methodology, secured component library, tooling, and threat modeling. Reach out for your security specialists at the beginning of a software project throughout the whole project and maintenance of your software. Consider leveraging the OWASP Software Assurance Maturity Model (SAMM) to help structure your secure software development efforts.

## How to Prevent
- Establish and use a secure development lifecycle with AppSec professionals to help evaluate and design security and privacy-related controls
- Establish and use a library of secure design patterns or paved road ready to use components
- Use threat modeling for critical authentication, access control, business logic, and key flows
- Integrate security language and controls into user stories
- Integrate plausibility checks at each tier of your application (from frontend to backend)
- Write unit and integration tests to validate that all critical flows are resistant to the threat model. Compile use-cases and misuse-cases for each tier of your application.
- Segregate tier layers on the system and network layers depending on the exposure and protection needs
- Segregate tenants robustly by design throughout all tiers
- Limit resource consumption by user or service

[Source: OWASP TOP 10 Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/)

## Cheatsheets
[Insecure Design Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a042021-insecure-design)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 3](/data-validation-&-encoding/3)
- [Data-validation-&-encoding 6](/data-validation-&-encoding/6)
- [Data-validation-&-encoding 8](/data-validation-&-encoding/8)
- [Data-validation-&-encoding 10](/data-validation-&-encoding/10)
- [Data-validation-&-encoding J](/data-validation-&-encoding/J)

### Authentication
- [Authentication 3](/authentication/3)
- [Authentication 4](/authentication/4)
- [Authentication 10](/authentication/10)

### Authorization
- [Authorization 2](/authorization/2)
- [Authorization 4](/authorization/4)

### Cryptography
- [Cryptography 3](/cryptography/3)
- [Cryptography 4](/cryptography/4)
- [Cryptography 5](/cryptography/5)

### Cornucopia
- [Cornucopia 3](/cornucopia/3)
