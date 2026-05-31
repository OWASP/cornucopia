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
3. Pin shared workflow components and actions to specific, verified digests rather than using mutable version tags or floating references like "latest."
4. Review changes to pipeline definitions before they are executed, just as you would for application code.
5. Use the configuration supported by your CI platform to limit secrets exposed in individual steps - ideally each step should only have access to the credentials it actually needs.
6. If possible, block or limit internet access from your runners to make exfiltration more difficult.

For detailed advice on how to mitigate threats related to the card, see the [OWASP SAMM and OWASP DSOMM](#mapping 'OWASP SAMM and OWASP DSOMM requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP SAMM](https://github.com/owaspsamm/core/tree/develop/model/activities) and [OWASP DSOMM](https://dsomm.owasp.org/mapping) documentation.

## Reading the mappings

Mappings use identifiers from [OWASP SAMM](https://owaspsamm.org/model/) and [OWASP DSOMM](https://dsomm.owasp.org/mapping).

SAMM identifiers specify a [Business Function, Security Practice and Stream](https://owaspsamm.org/about/). For example, I-SB-A breaks down as **I**mplementation - **S**ecure **B**uild - [Stream **A** (Build Process)](https://owaspsamm.org/model/implementation/secure-build/stream-a/), I-SD-A as **I**mplementation - **S**ecure **D**eployment - [Stream **A** (Deployment Process)](https://owaspsamm.org/model/implementation/secure-deployment/stream-a/), and O-EM-A as **O**perations - **E**nvironment **M**anagement - [Stream **A** (Configuration Hardening)](https://owaspsamm.org/model/operations/environment-management/stream-a/).

DSOMM identifiers specify a [Dimension and Sub-Dimension](https://dsomm.owasp.org/usage/). For example, I-DSC breaks down as **I**mplementation - **D**evelopment and **S**ource **C**ontrol, I-IH as **I**mplementation - **I**nfrastructure **H**ardening, BD-B as **B**uild and **D**eployment - **B**uild, and BD-D as **B**uild and **D**eployment - **D**eployment. A Sub-Dimension groups multiple related activities, and is used here because the activities as a group correspond to the card's scope.