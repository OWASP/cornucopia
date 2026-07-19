## Scenario: Invent Your Own Agentic AI Threat

You have identified an attack that misuses inherent Agentic AI functionality or a related design flaw. Inventing an Agentic AI threat can lead to:

1. **Prompt and Context Manipulation:** Attackers craft inputs that redirect agent intent, corrupt reasoning context, or extract confidential instructions.
2. **Excessive Agency Exploitation:** Agents are induced to take high-impact actions across integrated systems that exceed their intended authorization scope.
3. **Resource and Budget Abuse:** Autonomous tool-chaining or recursive planning exhausts compute budgets, API quotas, or financial limits.
4. **Agent Identity Spoofing:** Rogue or compromised peer agents issue instructions to other agents by impersonating legitimate orchestrators.
5. **Sandbox and Tooling Escape:** Weak tool input validation or sandboxing allows unintended code or system command execution.
6. **Sensitive Information Leakage:** System prompts, reasoning traces, or unauthorized data sources are exposed through adversarial interaction.
7. **Orchestration Layer Compromise:** Control over the scheduling or coordination plane is seized, enabling attacker-defined workflows at scale.
8. **Multi-Step Goal Hijacking:** Malicious intermediate objectives are injected into autonomous multi-step plans without detection.

## Threat Modeling

### STRIDE

The appropriate STRIDE category depends on the specific threat you create and the way the agent is misused.

### PHANTOM-B

An invented agentic AI threat can fit any PHANTOM-B prompt: **Prompt injection**, **Hallucination**, **Anthropomorphization**, **Non-explainability**, **Training issues**, **Over-reliance on the LLM**, **Missing security engineering**, or **Biases**.

### What can go wrong?

Agentic AI attacks combine the scale and speed of automated systems with the authority and cross-system reach granted to AI agents. A single successful attack can trigger cascading effects across all systems the agent is connected to, producing data loss, unauthorized transactions, service disruption, or persistent unauthorized access, often before any human reviewer notices the anomaly.

For other things that can go wrong, see [OWASP Top 10 for LLM, Top 10 for Agentic Applications, and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/), [OWASP Top 10 for Agentic Apps](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

Defenses for Agentic AI systems must address the full attack surface: the agent's inputs, its planning and reasoning process, its tool integrations, and its communication with other agents.

1. **Least-privilege agency:** Grant agents only the tools, data access, and action authority needed for the specific task — no more.
2. **Human-in-the-loop for high-impact actions:** Require explicit human confirmation before any irreversible or high-blast-radius action proceeds.
3. **Input and context validation:** Treat all agent inputs - prompts, retrieved content, tool output, agent messages — as untrusted until validated.
4. **Agent identity and message integrity:** Authenticate inter-agent communication and sign workflow definitions to prevent spoofing and injection.
5. **Resource budgets and circuit breakers:** Enforce hard limits on tool calls, API usage, and session duration to contain runaway or adversarially triggered execution.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.