## Scenario: ENIAC's get-rich-quick scenario

### Example

ENIAC has expensive tastes. They resell multiple services which web and mobile apps use to deliver specialist content. ENIAC especially likes the services which make commission-based payments because they can increase their revenues by automating use of their customers' web and mobile apps, and doing so continuously at scale. The customers even think their app is popular because of the high-use! ENIAC is careful to make the usage patterns per user look normal and controls the rate to avoid affecting performance of the apps. While the money rolls in, ENIAC is planning yet another no-expense spared holiday.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. ENIAC mis-uses the application's features by sending requests at large scale, which are not valid normal use.

### What can go wrong?

Attackers can use valid application features at scale, by crafting and sending requests that raise operating costs by inflating charges billed by the relevant service provider. The application owner suffers from increased charges, and thus lower operating margins. If the attacker is also the service provider, or able to compromise that in some way, the attacker can be the beneficiary of the inflated charges. Performance measures are no longer valid because usage data are compromised by the automated attack.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).


### What are we going to do about it?

- Monitor functionality use relative to other parts of the application, as well as metrics like outcome rations, service provider charges, and operating margins.
- Replace paid-for services with less expensive or free options.
- Define acceptable usage patterns and enforce limits to usage of chargeable service provider content/functionality.
- Consider requiring identification, re-authentication or some other increased authentication assurance for relevant functionality.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

