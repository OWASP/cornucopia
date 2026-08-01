## Scenario: Mark 1 Colossus's fast-forward to win scenario

### Example

Mark 1 Colossus gambles programmatically online. To make bets faster and more frequently Mark 1 Colossus has automated selecting games, choosing options and placing bets. This headless interaction skips past all manner of advertisements, tracking, upselling, intermediate confirmation steps and other distractions which the betting sites use to try to make more money. Mark 1 Colossus can focus on making bets, but the betting companies loose out.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. Mark 1 Colossus alters the designed application flow to their own advantage.

### What can go wrong?

Automation to increase speed/throughput, to progress through business logic faster, can be used to violate applications' normal use to achieve individual gain, or loss to some other party. 

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor usage for hastened progress through business logic.
- Define acceptable usage patterns, compel users to complete all required steps, and enforce limits to rate of usage.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
