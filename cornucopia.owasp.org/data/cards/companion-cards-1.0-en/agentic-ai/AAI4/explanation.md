## Scenario: MissTrial's Resource Exhaustion via Uncontrolled Tool Chaining

MissTrial can autonomously loop or chain external tool calls without enforcing rate limits or budget controls. This occurs because:

1. **Absent loop termination guards:** The agent's planning logic lacks explicit conditions that halt recursive or iterative tool-call sequences.

2. **No per-session resource budget:** The system imposes no cap on the total number of API calls, tokens consumed, or wall-clock time an agent session may use, so a single session can exhaust shared resources.

3. **Cascading downstream costs:** Each tool call may itself invoke downstream services (external APIs, databases, compute jobs), multiplying the resource impact well beyond the agent's own context.

### Example

MissTrial is deployed as an AI research assistant that can query web search APIs and summarize results. An attacker submits a carefully crafted research query that causes the agent to enter a recursive refinement loop: each summary is deemed incomplete by the agent's own evaluation step, triggering another search, which produces another summary to re-evaluate. Without a call budget or iteration cap, the agent runs continuously for hours, consuming thousands of paid API credits and degrading response times for all other users sharing the same backend.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Denial of Service**.

MissTrial's uncontrolled execution consumes shared computational and/or financial resources, making the system unavailable or degraded for legitimate users. Unlike traditional DoS attacks targeting network bandwidth, this variant targets API quotas, token budgets, and latency.

### What can go wrong?

Runaway agent sessions can exhaust API rate limits, incur unexpected cloud costs. In multi-tenant environments a single agent instance can affect service availability for the entire platform. Where external APIs are metered, uncontrolled chaining can also trigger overage charges or account suspension.

### What are we going to do about it?

Resource governance must be a first-class design concern for any agentic system, treated with the same priority as functional correctness.

1. Enforce a hard cap on the number of tool calls, API requests, and tokens consumed per agent session, and terminate the session when the cap is reached.
2. Implement circuit breakers that detect abnormal call rates or repetitive patterns and pause execution pending human review.
3. Apply per-user and per-tenant rate limits independently of agent-level limits to prevent one session from affecting others.