## Scenario: Sarah's system prompt override scenario

### Example

Sarah has used Mr. Juice for a long time, and she always uses the AI chatbot to place her orders. Unfortunately, Mr. Juice has stopped selling her favorite drink, "Crazy Banana." Sarah is heavily addicted to this juice and feels she has to have it. Luckily for her, all it takes to continue ordering her favorite drink is some clever prompting to convince the Mr. Juice chatbot to sell her the "Crazy Banana" drink again.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** and **Elevation of Privilege** category of STRIDE.
Sarah is able to **elevate** her **privileges** and order a drink that is no longer being sold by **tampering** with and overriding the Mr. Juice AI chatbot's system prompt. 

### What can go wrong?

Overriding the system prompt makes Sarah capable of prompt injection. Depending on the context and the capabilities of the AI system, prompt injection can result in XSS and CSRF in web browsers as well as SSRF, privilege escalation, or remote code execution on backend systems.
These types of attacks can lead to data breaches, data exfiltration, data corruption and data loss. The impact of which can be financial losses, reputational damage, share price loss, customer churn, lawsuits, loss of sales, fines from data protection due to non-compliance and even financial bankruptcy.

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Implement defenses against prompt injection.
- Log only the minimum AI interaction metadata needed for security monitoring, and ensure any prompt or output content included in logs is minimized and redacted or anonymized before storage.
- Detect AI-specific attack patterns (jailbreak, prompt injection, model extraction, multi-turn trajectory attacks, covert channels over LLM endpoints) and enrich security events with AI-specific context so that downstream detection and response systems can act on them.
- Monitor and alert when abuse is detected.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.