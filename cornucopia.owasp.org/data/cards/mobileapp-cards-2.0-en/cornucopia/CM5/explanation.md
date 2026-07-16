## Scenario: Debarghaya can reduce app users' privacy because the app repurposes personal information — such as device IDs, IP addresses, or behavioural patterns — collected for security concerns in order to cater for commercial interests without consent

Consider a scenario where Debarghaya works for a company that built a mobile banking app. The security team collects device fingerprints (device ID, OS version, screen resolution, IP address, installed app list) to detect fraud and bot activity. The marketing team notices this data is collected and requests access to build advertising profiles. The device fingerprint data is repurposed for targeted advertising without informing users or obtaining new consent for this additional purpose. The data was collected with a security purpose. It is now used for a commercial purpose. The users never agreed to this.

1. Data collected for one purpose (security, fraud prevention) repurposed for another (advertising, analytics) without consent violates the purpose limitation principle.
2. Device IDs and behavioural patterns are persistent identifiers that can be used to track users across apps and sessions even when other identifiers are reset.
3. Legitimate Interest is not a valid legal basis for repurposing security data for marketing without a balancing test.

### Example

Debarghaya discovers the banking app's fraud-detection dataset — including IP addresses, login times, device fingerprints, and transaction patterns — has been shared with the parent company's advertising division. Users' financial behaviour patterns are being used to target insurance and loan advertisements. The privacy policy said "we use your data for security and fraud prevention." It did not say "we share security data with our advertising partners." The purpose limitation was violated.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and involves privacy rights violations.

Repurposing security-collected data for commercial use without disclosure or consent violates regulatory requirements and erodes the trust that justifies the original security data collection.

### What can go wrong?

- Regulatory fines for purpose limitation violations (GDPR Article 5(1)(b)).
- User trust damage when repurposing is discovered.
- Sensitive financial, health, or behavioural data used to discriminate against or target vulnerable users.

### What are we going to do about it?

- Document the purpose of each data collection in the data inventory; enforce purpose limitation technically (separate data stores, access controls for different business units).
- Obtain separate, specific consent for each distinct purpose; "security and fraud prevention" does not include advertising.
- Apply the GDPR compatibility assessment when considering repurposing: purpose is only compatible with the original if there is a clear link, appropriate safeguards, and user expectation.
- Do not share security-collected data with commercial partners without a separate legal basis and disclosure.
