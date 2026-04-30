## Scenario: Samantha's expensive and computational resource intensive exhaustion scenario

### Example

Samantha is an avid Vibe coder. She does a lot of coding using LLM, but she can't afford a premium account. Luckily, she has found out that her favorite juice shop allows her to integrate it into her IDE after having written an IDE plugin that allows her to exploit it. With a bit of jailbreaking config, the AI chatbot becomes a full-blown LLM coding engine. So with a bit of prompting, she can spin up a couple of agents that solve all her coding tasks. Such a useful IDE plugin should be shared on GitHub. Before long, one thousand avid Vibe coders hammer the chatbot until its company credit card gets blocked by its AI chatbot provider. 

## Threat Modeling

### STRIDE

This scenario falls into the **Denial of Service** category of STRIDE.
Samantha can make requests of the AI chatbot until the application gets involuntarily shutdown.

### What can go wrong?

In AI systems, attackers can craft specific inputs or interactions that intentionally cause resource-intensive processes, potentially resulting in denial-of-service (DoS) conditions. LLMs can also involve significant costs. These costs can become substantial, especially in multi-agent systems. 

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Implement Rigorous Input Validation: Enforce strict size limits on all user-submitted data at the API gateway level, before it reaches the model.
Deploy Effective Rate-Limiting and Throttling: Use API gateways or middleware to enforce per-user or per-IP rate limits. Implement circuit breakers to automatically halt requests to downstream services that are failing.
- Establish Clear Resource Quotas: Define and enforce resource quotas (CPU, memory) for each AI model or service at the container orchestration level (e.g., Kubernetes).
- Monitor Infrastructure and Costs Continuously: Use monitoring tools to track resource consumption and API response times. Set up automated alerts for unusual spikes.
- Implement Spending Thresholds: For all third-party AI services, configure hard spending limits and billing alerts in the provider's console. Treat this as a critical security control.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AISVS](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AITG](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.