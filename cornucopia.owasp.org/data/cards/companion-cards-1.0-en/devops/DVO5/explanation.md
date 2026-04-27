## Scenario: Brian's Escape from Workload Isolation

Consider a scenario where Brian escapes the runtime isolation of a workload to access host resources, execute privileged operations, or attack other internal systems. This vulnerability arises from:

1. **Weak Isolation Boundaries:** The runtime environment does not enforce strong enough isolation between workloads and the underlying host.

2. **Misconfigured Privileges:** Workloads run with elevated privileges or capabilities that allow them to interact with host resources or other workloads.

### Example

Brian discovers that a workload running in a containerized environment has been granted excessive capabilities, including access to the host's filesystem. By exploiting this misconfiguration, he escapes the container's isolation boundary and gains access to the host system. From there, he reads credentials stored on the host, accesses other workloads running on the same machine, and moves laterally through the infrastructure. In another variation, workloads share a persistent, non-ephemeral runner where previous builds leave behind files and credentials that Brian's workload can access, effectively bypassing any intended isolation.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege**.

**Elevation of Privilege** occurs when an attacker gains access to resources or capabilities beyond their intended scope. Brian's workload is supposed to be confined to its isolated runtime environment, but by escaping that boundary, he gains access to host resources and other systems - a direct escalation of privilege.

### What can go wrong?

Isolation failures expose the entire host and potentially the wider infrastructure to compromise. This can manifest in various forms, including but not limited to:

- Access to host filesystem, credentials, or network from within a workload
- Lateral movement to other workloads or systems sharing the same host or network
- Exfiltration of secrets or data from the host environment
- Compromise of the orchestration or management layer through an escaped workload
- Contamination of shared or persistent build environments where one workload's artifacts affect another

### What are we going to do about it?

1. Run workloads with the minimum necessary privileges and capabilities. Avoid running as root or granting host-level access.
2. Use ephemeral, single-use runners or execution environments for build and deployment tasks so that one job's leftovers cannot affect the next.
3. Make use of the runtime's security features to restrict what workloads can do: limit filesystem access, network access, and system calls.
4. Review your workload configurations to check for excessive privileges or capabilities that are not actually needed.
5. If certain workloads handle sensitive data or operations (e.g., signing your artifacts), consider running them on dedicated hosts or in more tightly isolated environments.
6. Keep the runtime and host environment up to date with security patches to reduce the risk of known isolation bypass vulnerabilities.
