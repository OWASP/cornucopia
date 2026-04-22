## Scenario: Nariman's Manipulation of Pipeline Execution

Consider a scenario where Nariman gains control over pipeline execution by injecting malicious commands through manipulated CI configuration files or poisoned workflow dependencies. This vulnerability arises from:

1. **Manipulable CI Configuration:** Pipeline definition files can be modified by users who should not have control over how the pipeline executes.

2. **Unvalidated Workflow Dependencies:** The pipeline uses shared actions or workflow components that can be poisoned or typosquatted to execute malicious commands.

### Example

Nariman submits a pull request that modifies the CI configuration file to inject additional commands into the build step. The pipeline is configured to run on pull requests without restricting what the CI configuration can do, so Nariman's modified pipeline definition is executed with the pipeline's full credentials and access. The injected commands exfiltrate environment variables containing secrets and establish a connection to an external system, all within the context of a seemingly routine pull request.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering** and **Elevation of Privilege**.

**Tampering** applies because Nariman modifies the pipeline's behavior by altering its configuration or injecting commands, changing what the pipeline does.

**Elevation of Privilege** fits because the injected commands execute with all of the pipeline's credentials and permissions, which are typically more powerful than what the attacker would have as a regular contributor.

### What can go wrong?

Pipeline manipulation gives attackers a powerful execution context with broad access to secrets, infrastructure, and deployment targets. This can manifest in various forms, including but not limited to:

- Exfiltration of secrets and credentials available to the pipeline
- Execution of arbitrary code in a trusted environment with elevated permissions
- Modification of build outputs or deployment targets from within the pipeline
- Persistent compromise if pipeline modifications go undetected

### What are we going to do about it?

1. Treat pipeline configuration files like code: review changes to them with the same rigor, and restrict who can modify them.
2. Where feasible, run pipelines with reduced permissions and without access to production secrets. Ensure your pipeline configuration does not allow forks to use its credentials.
3. Pin shared workflow components and actions to specific, verified digests rather than using mutable references like "latest."
4. Review changes to pipeline definitions before they are executed, just as you would for application code.
5. Use the configuration supported by your CI platform to limit secrets exposed in individual steps - ideally each step should only have access to the credentials it actually needs.

