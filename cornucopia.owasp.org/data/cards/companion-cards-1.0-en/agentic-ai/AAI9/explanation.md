## Scenario: CoPirate's Unauthorized System Modification via Excessive Autonomy

CoPirate can modify configurations, permissions, or system settings beyond intended authorization due to excessive autonomy. This occurs because:

1. **Overly broad action scope:** The agent is granted write access to system configuration interfaces, permission management APIs, or infrastructure settings that are not required for its primary task.

2. **No authorization boundary on configuration actions:** The system does not distinguish between read operations and destructive or privileged write operations when the request originates from an AI agent, applying the same access level to both.

3. **Absent human approval gate for sensitive operations:** Configuration changes and permission modifications proceed automatically without requiring operator or admin confirmation, removing the last safeguard against unintended state changes.

### Example

CoPirate is deployed as an IT operations assistant that can query system health metrics and restart services. Over time, its toolset is expanded to include access to a cloud infrastructure API "for convenience." When a user asks CoPirate to "fix the permission issue causing the deployment failure," the agent interprets this broadly and modifies IAM role bindings in the cloud environment, granting a service account production-level permissions to resolve the immediate error. The change resolves the deployment but leaves a persistent over-privileged role that an attacker later discovers and exploits to access production data.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

CoPirate changes configurations, permissions, or role bindings in a way that increases access rights beyond what the original user or operator was authorized to grant. This is elevation of privilege because the agent may create or preserve over-privileged identities and access paths that allow unauthorized actions. 

### What can go wrong?

Unauthorized configuration changes can silently degrade the organization's security posture, creating persistent vulnerabilities that outlast the agent session that caused them. Over-permissioned roles, disabled security controls, or misconfigured access policies may go undetected until exploited. 

### What are we going to do about it?

Agents must operate under the same change-management controls applied to human administrators, with additional automated guardrails appropriate to autonomous operation.

1. Restrict agent tool access to the minimum set required for the task. Agents performing monitoring or reporting tasks should not have write access to configuration or permission systems.
2. Require explicit human approval for any agent action that modifies security-relevant configuration, permissions, or infrastructure state.