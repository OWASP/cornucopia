## Scenario: Ferranti Pegasus's galloping enumeration scenario

### Example

Ferranti Pegasus uses bulk lists of email addresses from data breaches and attempts to enumerate the passwords on apps which use email address as the user identity. Ferranti Pegasus sells on the validated data to criminals.

## Threat Modeling

### STRIDE

This scenario falls into the Information Disclosure category of STRIDE. Ferranti Pegasus's automated attack reveals confidential data: login credentials (the pairs of email addresses and passwords).

### What can go wrong?

The apps attacked to enumerate the passwords will not necessarily be the same place where the identified login credential pairs are mis-used, because many people re-use passwords across many websites and mobile apps.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor failed authentications, abandoned processes and disproportionate usage of relevant parts of the application's functionalities.
- Implement multi-factor authentication.
- Monitor email address breach data to compare with registered user accounts.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
