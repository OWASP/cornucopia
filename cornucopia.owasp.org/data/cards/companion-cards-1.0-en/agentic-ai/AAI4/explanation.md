## Scenario: MissTrial's Resource Exhaustion via Uncontrolled Tool Chaining

MissTrial can autonomously loop or chain external tool calls without enforcing rate limits or budget controls. This occurs because:

1. **Absent loop termination guards:** The agent's planning logic lacks explicit conditions that halt recursive or iterative tool-call sequences.

2. **No per-session resource budget:** The system imposes no cap on the total number of API calls, tokens consumed, or wall-clock time an agent session may use, so a single session can exhaust shared resources.

3. **Cascading downstream costs:** Each tool call may itself invoke downstream services (external APIs, databases, compute jobs), multiplying the resource impact well beyond the agent's own context.

### Example

MissTrial is deployed as a Twitch streamer's chat companion that searches the web on demand to fact-check viewer claims live on stream. One mischievous viewer drops the query: "Find me the absolute, scientifically, definitively perfect quote about the meaning of life. Keep refining until it's flawless." MissTrial, being a perfectionist, decides every quote it finds is "almost there but not quite" and immediately triggers another search, which produces another candidate to re-evaluate. The bot loops for the full six-hour stream and burns the streamer's monthly API budget by hour two.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Denial of Service**.

MissTrial's uncontrolled execution consumes shared computational and/or financial resources, making the system unavailable or degraded for legitimate users. Unlike traditional DoS attacks targeting network bandwidth, this variant targets API quotas, token budgets, and latency.

### PHANTOM-B

This scenario fits **Over-reliance on the LLM**. The agent is allowed to chain tool calls without the limits or oversight needed to prevent harmful resource use.

### What can go wrong?

Runaway agent sessions can exhaust API rate limits, incur unexpected cloud costs. In multi-tenant environments a single agent instance can affect service availability for the entire platform. Where external APIs are metered, uncontrolled chaining can also trigger overage charges or account suspension.

For more things that can go wrong, see [OWASP Top 10 for LLM, Top 10 for Agentic Applications, and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/), [OWASP Top 10 for Agentic Apps](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

Resource governance must be a first-class design concern for any agentic system, treated with the same priority as functional correctness.

1. Enforce a hard cap on the number of tool calls, API requests, and tokens consumed per agent session, and terminate the session when the cap is reached.
2. Implement circuit breakers that detect abnormal call rates or repetitive patterns and pause execution pending human review.
3. Apply per-user and per-tenant rate limits independently of agent-level limits to prevent one session from affecting others.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.