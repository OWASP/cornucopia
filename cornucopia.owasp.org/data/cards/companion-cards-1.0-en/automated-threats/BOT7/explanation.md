## Scenario: Manchester Mark 1's pop-the-register scenario

### Example

Manchester Mark 1 uses recently validated stolen payment cardholder data to "dip their hand" in online retailers' tills. Manchester Mark 1 does this by assembling and using the card data to buy stacks of higher-value, easily re-sold, goods like machines of various sorts. Upon delivery, the goods are promptly pushed onto the black market for cash.

## Threat Modeling

### STRIDE

This scenario falls into the **Spoofing** category of STRIDE. Manchester Mark 1 is pretending to be the true payment cardholder, but the details have actually been stolen, gaining access to the goods.

### What can go wrong?

Automated use of stolen data in bulk to obtain cash or good often leaves the merchant/operator to pick up the bill, because of consumer protection legislation. In some cases this may facilitate money laundering with action being taken against the merchant/operator by financial regulators.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor demand for higher-value goods/services, chargeback rates, usage of interlinked accounts and transactions between related accounts.
- Consider requiring identification, re-authentication or some other increased authentication assurance for relevant functionality.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
