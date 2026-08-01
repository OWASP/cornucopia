## Scenario: Manchester Baby's ham-spam scenario

### Example

Manchester Baby is a mischievous bot set up to disrupt social media, discussion forums and blogs that refer to "ham". It automatically finds and posts replies with jokey and inappropriate comments to any mention of the word "ham" causing annoyance and sometimes offense.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. Manchester Baby injects content into discussion threads.

### What can go wrong?

Additional automated content can be an annoyance, mischievous, disruptive and even malicious. The effects depend both on the purpose of the application and the type of content added, and its frequency.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor and track trends for content addition by users.
- Consider content moderation.
- Consider requiring identification, re-authentication or some other increased authentication assurance for functionality allowing addition of content.
- Actively remove spam content and block users.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
