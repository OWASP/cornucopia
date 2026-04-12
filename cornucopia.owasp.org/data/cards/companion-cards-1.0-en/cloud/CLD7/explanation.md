## Scenario: Jon's Escape from a Compromised Container

Jon exploits a container escape vulnerability to break out of an isolated container environment and gain direct access to the underlying cloud host. This occurs because:

1. **Container Running as Root or with Excessive Capabilities:** The container is configured to run as the root user or has been granted Linux capabilities that provide pathways to interact with the host kernel.

2. **Privileged or Host-Mounted Volumes:** The container is started in privileged mode, or sensitive host paths  are bind-mounted into the container, breaking the isolation boundary.

3. **Unpatched Container Runtime or Host Kernel:** The container runtime or the host kernel has a known vulnerability that permits a process within the container to escape to the host.

### Example

Jon gains code execution within a containerized microservice through a remote code execution vulnerability in a third-party library. He inspects the container's environment. Jon uses the available Docker client to start a new privileged container with the host filesystem mounted beneath it. From within this privileged container, he reads the host's cloud instance credentials from the instance metadata service, retrieves SSH keys from the host filesystem, and installs a reverse shell on the host, effectively escaping the container and establishing persistent access to the underlying cloud compute instance.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

Jon begins with limited, application-level access within a container and escalates to full control of the underlying host. The container escape exploits misconfigurations or vulnerabilities in the isolation layer that was intended to confine him. From the host, Jon may then escalate further into the cloud environment using instance credentials.

### What can go wrong?

Container escape attacks break the fundamental security boundary that containerization is designed to provide. Once an attacker reaches the host, they can access all other containers running on the same node, read instance credentials from the cloud metadata service, modify the host's filesystem and network configuration, and pivot into the broader cloud account. In managed Kubernetes environments, compromising a node can provide access to secrets mounted in other pods and the Kubernetes control plane.

### What are we going to do about it?

Harden container configurations to enforce isolation and prevent privilege escalation.

1. Run containers as non-root users and drop all Linux capabilities that are not explicitly required; never use privileged mode in production.
2. Keep container runtimes, base images, and host kernels patched and up to date, and use image scanning to detect vulnerable dependencies before deployment.
3. Deploy workloads on hardened nodes where possible and use a container security platform to detect anomalous behavior such as unexpected privilege escalation or filesystem modifications at runtime.
