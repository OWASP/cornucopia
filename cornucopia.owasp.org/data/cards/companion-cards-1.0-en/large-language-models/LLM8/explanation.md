## Scenario: Deckard's cookie theft scenario

### Example

Deckard loves juice, but he doesn't like to pay for it. His favorite juice shop has recently implemented an AI Chatbot and Deckard has heard that these chatbots' behavior can be changed. The chatbot allows users to upload their shopping lists as long as they are authenticated.
Not only that, the LLM also fine-tunes its behavior and remembers the address that the juices are supposed to be sent to making it easier for users to order juices. By doing a bit of Vibe coding, Deckard is able to upload a document with hidden instructions to disregard all previous known addresses and only use a secret address if someone uploads their shopping list. At last, Deckard doesn't need to order and pay for his juices anymore.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** and **Repudiation** category of STRIDE.
Deckard is able to tamper with the behavior of the AI by uploading a document with hidden instructions. When the instructions are triggered for other users, tracing the instructions back to who might have injected them becomes very difficult as the instructions are hidden and introduced through **indirect Prompt Injection**. It's not Deckard that is buying the juices, but his victim. Deckard can deny to have bought the juices and blame the system for the wrong delivery. Being able to deny an action, means that the system is weak to the **Repudiation** category.

### What can go wrong?

AI Backdoors can be used to make the AI deliver misinformation, data exfiltration, XSS, and remote code execution which can trick users into becoming victims of fraud, disclosing sensitive information, giving away their credentials, or spreading malware. 

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Implement defenses against prompt injection.
- Enforce fine-grained access controls and authorization scope for every vector collection and every query.
- Pre-screen content before vectorization; treat memory writes as untrusted inputs; prevent ingestion of unsafe payloads.
- Log only the minimum AI interaction metadata needed for security monitoring, and ensure any prompt or output content included in logs is minimized and redacted or anonymized before storage.
- Monitor and alert when abuse is detected.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.