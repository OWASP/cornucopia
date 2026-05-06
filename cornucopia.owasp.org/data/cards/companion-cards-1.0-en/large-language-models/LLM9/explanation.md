## Scenario: Rossum's insecure plugin abuse scenario

### Example

Rossum has recently partnered with Tyrell to start up a Juice shop business to compete with Mr. Juice. Competition is fierce and cash is low and something has to be done about it. Rossum has heard from Tyrell that the AI chatbot has some security weaknesses. He decides to investigate this further. He discovers that the authenticated version of the chatbot allows the user to see his pending unpaid invoices by connecting to the invoice database. This can't be functionality that comes out-of-the-box, but something Mr. Juice's developers have built. After experimenting with the prompt he is able to retrieve the invoices for all Mr. Juice's customers. He ends up creating an email list with all the customers, changing the account number on the invoices, and sending these customers a payment reminder. Finally, cash is pouring in and not out.

## Threat Modeling

### STRIDE

This scenario falls into the **Information Disclosure** and **Elevation of Privilege** category of STRIDE.
Rossum is able to disclose the invoices for all Mr. Juice's customers through privileges he should not have because the developers at Mr. Juice have implemented a plugin with an insecure integration design making data exfiltration possible. The plugin connects to the invoice database to retrieve the invoice on behalf of the customer, and missing access checks and loose privileges allows Rossum to elevate his own privileges.
If the plugin also is allowed to change and delete data from the invoice database, then the **Tampering** would also be applicable.

### What can go wrong?

Insecure plugins can lead to data exfiltration of sensitive information, that can trick users into becoming victims of fraud, identity theft, phishing, and spreading malware.

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Make sure all model artifacts are cryptographically signed by authorized entities.
- All artifacts used to configure plugins, MCP servers, skills, agents and teams should be stored in version control, code reviewed, and approved before deployment.
- Model training and fine-tuning environments should be isolated from production model endpoints, agent orchestration services, tool/MCP servers, and live RAG data sources.
- All high-risk AI operations (model deployment, weight export, training data access, production configuration changes) should require step-up authentication with session re-validation.
- Constrain tool execution, loading, and outputs to prevent unauthorized system access and unsafe side effects.
- All access control decisions are enforced by application logic or a policy engine, never by the AI model itself, and model-generated output must never override or bypass those decisions.
- Ensure MCP clients, plugins, tools and AI integrations have implemented a centralized authorization framework and that clients present valid credentials for every request.
- Log only the minimum AI interaction metadata needed for security monitoring, and ensure any prompt or output content included in logs is minimized and redacted or anonymized before storage.
- Monitor and alert when abuse is detected.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.