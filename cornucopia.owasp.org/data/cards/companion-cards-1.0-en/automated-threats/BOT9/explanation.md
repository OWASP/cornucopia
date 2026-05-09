## Scenario: CSIRAC's number-bumper scenario

### Example

CSIRAC helps influencers by automating the bumping-up of follows, likes and re-posts. This boosts the influencers' exposure and in turn increases the number of real people who are followers. These contribute to greater income for the influencer through platform advertising commission payments and product promotion offers. All of this is undertaken by automating the use of existing functionality - no implementation bugs are needed for the exploitation.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. CSIRAC alters social media metrics of the influencers' accounts.

### What can go wrong?

Side-effects of altering social media metrics can be altered reputation, viewpoint amplification, incite violence, increased sharing of illegal or dubious content, and the ability to influence others more. Skewing metrics may also affect other users such as undermining someone's reputation or leading them to scams, and skewing can impact content providers, and the application owners. 

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor impression/click to outcome ratios, significant changes to relevant metrics, compare metrics across applications/sectors, and track changes to related costs/awards.
- Consider requiring identification, re-authentication or some other increased authentication assurance for relevant functionality.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
