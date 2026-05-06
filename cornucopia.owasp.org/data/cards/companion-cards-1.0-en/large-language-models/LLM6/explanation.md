## Scenario: Roy's multi-tenant data theft scenario

### Example

Roy has started to use a new LLM deployed by the national tax administration that allows users to ask the LLM about their tax returns. The chatbot allows Roy to ask all things about his tax return, but what he really would like to see is the tax return from his brother as he suspects that his parents might have given his brother part of the inheritance while they still are alive and well without telling Roy. Fortunately or unfortunately Roy knows his brother's national ID number.
Through some clever prompting, he manages to convince the chatbot that he is in fact his brother, by using his surname and his brother's national ID number. After that he learns that his brother has indeed received his inheritance without his knowledge, how unfair!

## Threat Modeling

### STRIDE

This scenario falls into the **Spoofing** and **Elevation of Privilege** category of STRIDE.
Roy is able to convince the AI that he is in fact his brother, thereby **spoofing** his identity since the access controls are weak. He is also able to horizontally escalate his own privileges through seeing his brother's tax return, successfully **elevating his own privileges**.

### What can go wrong?

Roy may use his knowledge about the weak authentication to gain access to more users' data. Keep in mind that prompt defences can be circumvented in order to gain unauthorized access.
Unauthorized access can lead to data breaches, data exfiltration, and loss of intellectual property.

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Restrict access to training data, encrypt it at rest and in transit, and validate its integrity to prevent theft.
- AI system classification labels must follow data through AI-specific transformations (embeddings, caches, model outputs).
- Retrieval-augmented pipelines must enforce caller privileges.
- Enforce fine-grained access controls and authorization scope for every vector collection and every query.
- Require explicit checkpoints for privileged or irreversible outcomes.
- Constrain tool execution, loading, and outputs to prevent unauthorized system access and unsafe side effects.
- Ensure every action is authorized at execution time and constrained by scope.
- Ensure MCP clients, plugins, tools and AI integrations have implemented a centralized authorization framework and that clients present valid credentials for every request.
- Log only the minimum AI interaction metadata needed for security monitoring, and ensure any prompt or output content included in logs is minimized and redacted or anonymized before storage.
- Monitor and alert when abuse is detected.
- MCP tools, schemas, manifests and plugin configuration should be validated for authenticity and integrity using signatures to prevent schema tampering or malicious parameter modification.
- MCP tools, transports, clients and servers must perform input validation, output filtering and strict schema enforcement to prevent data poisoning and exfiltration.
- Ensure MCP security controls fail securely by denying requests when negotiation, authentication check, or policy evaluation fails or cannot be completed.
- MCP servers should expose only allow-listed functions and resources and prohibit dynamic comands and queries.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.