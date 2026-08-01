## Scenario: EDSAC's sneaky scenario

### Example

EDSAC loves sneakers. The best ones quickly sell out from brand websites, online marketplaces, and vintage resellers apps. EDSAC monitors all these online sites for suitable product, and uses automation to buy up the most exclusive and sought-after items, doing so at scale and speed which people could not achieve.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. EDSAC acquires sought-after, often limited-availability, items by using the application in ways normal users would be unable to do manually.

### What can go wrong?

Stock is sold-out quickly, leading to a type of user denial of service. There may be unusual high peaks of activity for certain limited-availability goods or services, and subsequently increased circulation of these items on secondary markets.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor stock depletion rates and availability of items on secondary markets.
- Limit rapid/repeated purchases by users.
- Consider requiring identification, re-authentication or some other increased authentication assurance for relevant functionality.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
