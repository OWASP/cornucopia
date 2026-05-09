## Scenario: UNIVAC 1's population-explosion scenario

### Example

UNIVAC 1 automates the registration, verification and profile generation of huge numbers of user accounts. Criminals pay UNIVAC 1 to do this on many different types of website and pays per hundred accounts created. The accounts are used for mis-use later.

## Threat Modeling

### STRIDE

This scenario falls into the **Elevation of Privilege** category of STRIDE. UNIVAC 1 creates user accounts, having higher privileges than unregistered users, and which provide access to additional application functionality.

### What can go wrong?

Fake accounts do not contribute to valid use of applications, and could be used subsequently to generate spam, launder cash or goods, spread malware, affect reputation, cause mischief, or skew content, reviews and surveys.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor account creation rate, accounts with incomplete information, use of fake/stolen profile data, unused accounts, accounts which subsequently mis-use the application
- Consider limiting functionality available to newly created, or under-used, accounts.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
