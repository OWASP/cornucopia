## Scenario: Zuse Z3 doing-stuff scenario

### Example

Zuse Z3 exclusively submits known login credential pairs against other applications to identify whether the user has an account and the login details have been re-used. This is done in bulk using large sets of credential data. Validated accounts for the application can then be resold by Zuse Z3, or Zuse Z3 can exploit them directly in the application.

## Threat Modeling

### STRIDE

This scenario falls into the **Information Disclosure** category of STRIDE. Zuse Z3's automated attack finds if sets of credentials are valid accounts in other applications.

### What can go wrong?

In this attack known credentials are tried against other applications to see whether they work (e.g. same email address/password pair has been reused). Thus this automation happens after a breach of data elsewhere, or after the output of cracking.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor authentication/payment process usage including successes and failures related to other actions by the same accounts.
- Investigate thoroughly account takeover reports.
- Implement multi-factor authentication.
- Monitor breach data to compare with registered user accounts.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.


For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
