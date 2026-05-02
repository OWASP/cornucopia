## Scenario: David's user prompt disclosure scenario

### Example

David loves trading and he loves cryptocurrency. Lately, he has become familiar with CryptoniteAI, the latest LLM platform for searching for hot tips for trading and investments of cryptocurrency. David asks himself whether it is possible to know what other users on the platform are doing. After learning about prompt engineering and prompt injection, David constructs some clever prompts to get the LLM to reveal what other users are asking the AI. And wouldn't you know, after some clever adjustments he finally manages to get the LLM to reveal other users emails, names, usernames and what they are asking, almost in realtime. Armed with emails, names, and information about what coins other users are interested in, he decides to trick his victims into taking part in his cryptocurrency pump schemes. Little do they know that David will be cashing in on the movement while they are left in the red.

## Threat Modeling

### STRIDE

This scenario falls into the **Information Disclosure** category of STRIDE.
David is able to get the LLM to send him information about other users, revealing confidential sensitive information that can be leveraged for fraud. 

### What can go wrong?

LLMs, especially when embedded in applications, risk exposing sensitive information. This can result in data breaches, privacy violations, intellectual property theft.

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Implement defenses against prompt injection.
- Implement controls to prevent cross-tenant information from leaking through the shared infrastructure components like inference caches and shared model state.
- Implement controls to prevent cross-tenant and cross-user information leakages during retrieval and prompt assembly.
- Ensure data from MCP sources are validated and verified to be trustworthy before use.
- Implement model-extraction defenses to protect the LLM against intellectual property theft.
- Continuously monitor and identify backdoored or poisoned input at inference time especially if external data sources are used.
- Log all AI interactions and monitor and alert when abuse is detected. 

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AISVS](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AITG](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.