## Scenario: Pravir's Exploitation of Outdated Dependencies

Consider a scenario where Pravir exploits known vulnerabilities in outdated or poorly maintained dependencies used by the application, its repositories, or its DevOps infrastructure. This vulnerability arises from:

1. **Lack of Dependency Maintenance:** Dependencies are not regularly updated, leaving known vulnerabilities unpatched.

2. **Insufficient Visibility:** The team does not have a clear picture of what dependencies are in use and which have known issues.

### Example

Pravir identifies that a web application relies on a library version with a publicly disclosed vulnerability. The vulnerability has been known for months and a patch is available, but the team has not updated the dependency because they lack a process for tracking and applying dependency updates. Pravir exploits the vulnerability to gain unauthorized access to the application's internal functionality. The same pattern extends to the development infrastructure, where outdated dependencies in build tools and repository integrations create additional entry points.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege**.

**Elevation of Privilege** occurs when an attacker gains capabilities beyond what they should have. Exploiting a known vulnerability in an outdated dependency typically allows Pravir to perform actions or access resources that the application was not designed to allow, whether that is executing arbitrary code, accessing protected data, or bypassing security controls. The root cause is the unpatched vulnerability, and the impact is unauthorized capability.

### What can go wrong?

Outdated dependencies are one of the most common and exploitable weaknesses in modern software. This can manifest in various forms, including but not limited to:

- Exploitation of publicly known vulnerabilities with available exploit code
- Compromise of build tools or infrastructure through vulnerable development dependencies
- Difficulty in identifying affected systems when dependency inventories are incomplete
- Delayed patching due to fear of breaking changes, leaving vulnerabilities open longer

### What are we going to do about it?

1. Know what dependencies your project uses, including transitive ones. Your package manager's lock file is a good starting point.
2. Set up automated dependency scanning that alerts you when known vulnerabilities are found in your dependencies.
3. Make updating dependencies a regular part of your workflow, not something you only do when forced to. It's easier to make small, frequent upgrades than to deal with years of accumulated breaking changes.
4. Keep an eye on whether your dependencies are still maintained. If a library is abandoned or end-of-life, start planning a migration before it becomes urgent.
5. Don't forget about development and build tool dependencies, they are just as exploitable as your runtime dependencies.
6. Test dependency updates before deploying to production to avoid breaking things.
7. Keep the number of dependencies reasonable - every dependency you add is a dependency you have to maintain and trust.
8. Make sure internal systems are also covered by updates. Even if they're not exposed to the internet, they may be compromised by any attacker that gains access to the network through other means.

For detailed advice on how to mitigate threats related to the card, see the [OWASP SAMM and OWASP DSOMM](#mapping 'OWASP SAMM and OWASP DSOMM requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP SAMM](https://github.com/owaspsamm/core/tree/develop/model/activities) and [OWASP DSOMM](https://dsomm.owasp.org/mapping) documentation.

## Reading the mappings

Mappings use identifiers from [OWASP SAMM](https://owaspsamm.org/model/) and [OWASP DSOMM](https://dsomm.owasp.org/mapping).

SAMM identifiers specify a [Business Function, Security Practice and Stream](https://owaspsamm.org/about/). For example, O-EM-B breaks down as **O**perations - **E**nvironment **M**anagement - [Stream **B** (Patching and Updating)](https://owaspsamm.org/model/operations/environment-management/stream-b/), I-SB as **I**mplementation - [**S**ecure **B**uild](https://owaspsamm.org/model/implementation/secure-build/), I-DM-A as **I**mplementation - **D**efect **M**anagement - [Stream **A** (Defect Tracking)](https://owaspsamm.org/model/implementation/defect-management/stream-a/), and D-SA-B as **D**esign - **S**ecure **A**rchitecture - [Stream **B** (Technology Management)](https://owaspsamm.org/model/design/secure-architecture/stream-b/). Where the identifier only specifies up to a Security Practice, both streams are relevant to the card.

DSOMM identifiers specify a [Dimension and Sub-Dimension](https://dsomm.owasp.org/usage/). For example, BD-PM breaks down as **B**uild and **D**eployment - **P**atch **M**anagement, BD-D as **B**uild and **D**eployment - **D**eployment, and TV-SDA as **T**est and **V**erification - **S**tatic **D**epth for **A**pplication. A Sub-Dimension groups multiple related activities, and is used here because the activities as a group correspond to the card's scope.