## Scenario: EDVAC's dynamic-pricing scenario

### Example

EDVAC runs an online shop in a very competitive market sector.  Before becoming an online business they had a physical shop and used to go around other local shops to find out what competitors were selling the same or similar goods for. EDVAC has applied this same technique online - and does it automatically without human involvement. EDVAC created a web-scraping tool which continuously scrapes information from competitors' web stores, online marketplaces and sales  aggregators, which ensures EDVAC's pricing on its own online shop is customised minute-by-minute, based on regularly refreshed competitors' product pricing, discounts and availability data. This dynamic-pricing enables rapid reaction to any changing market conditions, and also enhanced profitability when supply is restricted elsewhere.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. EDVAC consumes content meant for real customers, at scale and for its own use, undermining the business by tempting customers away.

### What can go wrong?

The publication of pricing, discount, availability and other product data helps real customers make purchase decisions, but attackers can mis-use the information to their own benefit, and have adverse effects on the information provider such as lost business, and increased costs.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor product page use, bandwidth usage and business metrics like customer conversion rates.
- Consider removing some information.
- Consider capping rate of application use per session/user/Ip address etc.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
