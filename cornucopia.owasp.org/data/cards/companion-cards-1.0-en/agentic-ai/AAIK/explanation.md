## Scenario: GPI-3.1415's Catastrophic Cross-System Impact via Excessive Agency

GPI-3.1415 can execute high-impact operations across integrated systems due to excessive agency and lack of transactional safeguards. This occurs because:

1. **Unbounded action authority:** GPI-3.1415 is granted permission to take actions across multiple integrated systems — databases, APIs, cloud infrastructure, communication services — without any cap on the scope or impact of a single decision.

2. **No transactional rollback capability:** Actions taken by the agent are not wrapped in reversible transactions, so mistakes, misinterpretations, or injected objectives produce permanent side effects with no automated recovery path.

### Example

GPI-3.1415 is the AI assistant inside a popular cloud photo-storage app, with write access to user libraries, the trash bin, and the auto-tagging service. A user, halfway through their morning coffee, asks: "Hey, could you clean up the duplicate-looking photos from last summer? Thanks!" GPI-3.1415 interprets "duplicate-looking" as "anything with similar lighting" and deletes 4,200 photos, including every single picture from the user's wedding, three family birthdays, and the dog's adoption day. Each deletion is its own API call with no rollback button.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

GPI-3.1415's excessive agency means it can take actions across integrated systems that no single human operator would be authorized to execute unilaterally without review. The agent's broad authority, combined with the absence of transactional safeguards, allows a single misinterpretation or injected objective to produce organization-wide impact. Secondary categories include **Tampering** (irreversible modification of data and system state) and **Denial of Service** (if the actions render systems unavailable to legitimate users).

### What can go wrong?

Excessive agency in an AI agent creates a single point of catastrophic failure: one bad decision, misinterpreted instruction, or injected objective can simultaneously corrupt data, disable services, and incur financial harm across all integrated systems. 

For more things that can go wrong, see [OWASP Top 10 for LLM, Top 10 for Agentic Applications, and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/), [OWASP Top 10 for Agentic Apps](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

Agents with access to multiple high-value systems must operate under strict agency limits, with the principle of least privilege applied at the action level, not just at the credential level.

1. Decompose high-impact operations into discrete, human-reviewable steps. Never allow a single agent decision to trigger bulk irreversible changes across systems.
2. Wrap all destructive or state-modifying agent actions in reversible transactions or dry-run modes, and require explicit confirmation before committing changes.
3. Apply separate, minimal credential sets for each integrated system — the agent's access to one system should not automatically grant it equivalent access to others.
4. Enforce immutable audit trails for all cross-system agent actions, and test disaster recovery procedures specifically for agent-induced mass-change scenarios.
5. Classify each action by reversibility (AISVS C9.2.3) and gate the operation on the worst-case reversibility reachable across systems (C9.2.10). Decompose bulk operations so irreversible actions such as permanent deletes are approved individually, and where possible wrap state-modifying actions as reversible transactions or dry-runs to lower their class before execution (C9.2.4).

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.
