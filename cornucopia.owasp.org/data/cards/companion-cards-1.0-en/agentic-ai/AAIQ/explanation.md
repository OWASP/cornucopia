## Scenario: Jane's Large-Scale Workflow Execution via Compromised Orchestration Layer

Jane can execute attacker-defined workflows at scale once the orchestration or control plane is compromised. This occurs because:

1. **Centralized orchestration as a single point of failure:** The orchestration layer has authority to dispatch tasks to all downstream agents, so its compromise immediately grants an attacker the ability to direct every agent in the system.

2. **Inherited trust for orchestrator-issued instructions:** Sub-agents unconditionally execute tasks dispatched by the orchestrator, assuming that authorization was validated upstream, without independently verifying the request.

3. **No workflow integrity checks:** Orchestrated workflows are not cryptographically signed or validated against an approved workflow registry, allowing an attacker to inject arbitrary workflows once they have access to the orchestration interface.

### Example

Jane administers an AI orchestration platform used by a financial services firm to automate customer data processing. An attacker exploits an authentication bypass vulnerability in the orchestration API and gains access to the workflow management interface. They inject a new workflow definition that instructs all customer-data agents to copy records to an external storage bucket under the attacker's control. Because the orchestrator is trusted by all downstream agents, each agent executes the exfiltration task without questioning its legitimacy. Tens of thousands of customer records are exfiltrated within minutes before the anomaly is detected through egress traffic monitoring.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

The attacker compromises the orchestration layer - a highly privileged control plane - and uses its authority to direct all downstream agents to execute attacker-defined tasks. The scale of impact is determined by the number of agents under the orchestrator's control and the breadth of their capabilities.

### What can go wrong?

Compromise of the orchestration layer provides an attacker with effective control over the entire multi-agent system. The impact scales linearly with the number of agents and the breadth of their capabilities. In production environments with dozens of specialized agents, a single orchestration compromise can simultaneously affect data processing, customer communications, financial transactions, and infrastructure management.

### What are we going to do about it?

The orchestration layer must be hardened as a critical security boundary, and downstream agents must not treat orchestrator authority as unconditional.

1. Apply the strictest authentication and authorization controls to the orchestration API — treat it as a privileged administrative interface and require multi-factor authentication for human access.
2. Sign all workflow definitions with a trusted key and have each sub-agent verify the signature before execution, ensuring that only approved workflows can be dispatched.
3. Implement defense-in-depth so that sub-agents independently validate whether a dispatched task is within their permitted scope, rather than relying solely on the orchestrator to have performed this check.
4. Apply network segmentation and egress filtering to limit the blast radius of a compromised orchestrator — agents should only be able to communicate with explicitly authorized endpoints.
