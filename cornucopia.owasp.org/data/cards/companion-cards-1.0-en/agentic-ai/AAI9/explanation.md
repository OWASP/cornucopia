## Scenario: CoPirate's Unauthorized System Modification via Excessive Autonomy

CoPirate can modify configurations, permissions, or system settings beyond intended authorization due to excessive autonomy. This occurs because:

1. **Overly broad action scope:** The agent is granted write access to system configuration interfaces, permission management APIs, or infrastructure settings that are not required for its primary task.

2. **No authorization boundary on configuration actions:** The system does not distinguish between read operations and destructive or privileged write operations when the request originates from an AI agent, applying the same access level to both.

3. **Absent human approval gate for sensitive operations:** Configuration changes and permission modifications proceed automatically without requiring operator or admin confirmation, removing the last safeguard against unintended state changes.

### Example

CoPirate is deployed to help a small startup's brand-new junior dev manage their cloud environment. Over the months, the toolkit has been developed until CoPirate casually rewrite IAM roles. Late one Friday, the dev sighs at their screen and asks: "Hey CoPirate, just fix whatever permission thing is blocking my deploy, I want to go home." CoPirate, committed to solving the problem, grants the deployment service account full god-mode access to production. The deploy succeeds, the dev orders celebratory pizza, and three months later an attacker stumbles upon the still-active over-privileged role and helps themselves to the customer database.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

CoPirate changes configurations, permissions, or role bindings in a way that increases access rights beyond what the original user or operator was authorized to grant. This is elevation of privilege because the agent may create or preserve over-privileged identities and access paths that allow unauthorized actions. 

### PHANTOM-B

This scenario fits **Over-reliance on the LLM**. Excessive autonomy lets the agent change configurations, permissions, or settings beyond its intended authority which attackers can exploit, but this is only made possible through processes that are missing engineering principles like authorization, Segregation of Duties (SoD), and least privilege. You could therefor also argue that **Missing security engineering** is the root cause.

### What can go wrong?

Unauthorized configuration changes can silently degrade the organization's security posture, creating persistent vulnerabilities that outlast the agent session that caused them. Over-permissioned roles, disabled security controls, or misconfigured access policies may go undetected until exploited. 

For more things that can go wrong, see [OWASP Top 10 for LLM, Top 10 for Agentic Applications, and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/), [OWASP Top 10 for Agentic Apps](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

Agents must operate under the same change-management controls applied to human administrators, with additional automated guardrails appropriate to autonomous operation.

1. Restrict agent tool access to the minimum set required for the task. Agents performing monitoring or reporting tasks should not have write access to configuration or permission systems.
2. Require explicit human approval for any agent action that modifies security-relevant configuration, permissions, or infrastructure state.
3. Classify each configuration or permission action by reversibility (AISVS C9.2.3) and gate on it: read-only inspection can run unattended, while externally reversible or irreversible changes such as granting IAM roles require approval (C9.2.4). The reversibility class is declared on the action, not inferred by the agent at run time.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.
