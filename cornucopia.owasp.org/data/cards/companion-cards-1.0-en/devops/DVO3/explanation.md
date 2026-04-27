## Scenario: Aryan's Exploitation of a Poorly Hardened Internal Service

Consider a scenario where Aryan exploits an internal system or service that was not properly hardened from the start, or whose security configuration has degraded over time. This vulnerability arises from:

1. **Insufficient Initial Hardening:** The system was deployed with default configurations, unnecessary services enabled, or overly permissive settings.

2. **Configuration Drift:** Security settings that were once appropriate have drifted over time due to ad-hoc changes, updates, or lack of maintenance.

### Example

Aryan discovers that an internal service used for artifact storage still runs with its default administrative credentials and has several unnecessary network services exposed. The service was initially set up quickly to unblock a team and was never revisited. Over time, patches were skipped and the configuration was loosened to work around integration issues. Aryan leverages the default credentials to gain administrative access, then uses the exposed services to pivot to other internal systems.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering** and **Elevation of Privilege**.

**Tampering** applies because poorly hardened systems allow attackers to modify configurations, data, or behavior of the system in unauthorized ways.

**Elevation of Privilege** fits because Aryan exploits weak configurations, such as default credentials or unnecessary services, to gain a level of access he should not have.

### What can go wrong?

Insufficiently hardened systems create a broad attack surface within the internal infrastructure. This can manifest in various forms, including but not limited to:

- Exploitation of default credentials or known default configurations
- Unauthorized access through unnecessary exposed services or ports
- Privilege escalation through misconfigured access controls
- Lateral movement to other systems after compromising a poorly hardened service
- Persistent access due to unpatched vulnerabilities in internal tools

### What are we going to do about it?

1. Check if your organization has hardening baselines or guidelines for internal systems, and follow them. If none exist, start by changing default credentials, disabling unnecessary services, and locking down network access.
2. Define infrastructure and system configurations as code so they are version-controlled, reviewable, and reproducible. This also makes configuration drift easier to spot and fix.
3. Disable or remove unnecessary services, ports, and features from internal systems you manage.
4. Make sure internal services require proper authentication and are not accessible with default or shared credentials.
5. Don't forget to patch internal systems and DevOps infrastructure - not just the application itself.
6. Give service accounts only the permissions they actually need.