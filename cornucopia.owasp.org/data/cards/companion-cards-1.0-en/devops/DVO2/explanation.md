## Scenario: Aram's Undetectable Manipulation of Build and Deployment Processes

Consider a scenario where Aram carries out malicious actions targeting build, delivery, and deployment processes, and these actions cannot be properly investigated afterward. This vulnerability arises from:

1. **Insufficient Logging:** Security-relevant events in the build and deployment systems are not adequately recorded or are missing entirely.

2. **Easily Tampered Log Data:** Log data lacks integrity protections, allowing Aram to modify or delete evidence of his actions.

3. **Inaccurate Timestamps:** Event records lack reliable, synchronized timestamps, making it difficult to reconstruct the sequence of events.

4. **Insufficient Log Retention:** Collected logs are only stored for a short time, which may lead to them being fully or partially deleted before a breach is identified and investigated.

### Example

Aram gains access to a shared build system and modifies a build script to include a backdoor. The system does not log who changed the build configuration or when. After the modified build runs and deploys, the team notices the anomaly but cannot determine what was changed, by whom, or when it happened. The limited logs that do exist are stored in the same environment Aram has access to, so he is able to quietly remove any traces of his activity. Without accurate and protected audit trails, the incident investigation stalls and the team cannot determine the scope of the compromise.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Repudiation** and **Tampering**.

**Repudiation** occurs when an attacker can deny having performed an action because the system cannot prove otherwise. Aram's malicious actions cannot be attributed to him or even detected due to insufficient or missing logs.

**Tampering** applies because the audit trails themselves can be modified or deleted, undermining the integrity of the evidence needed for investigation.

### What can go wrong?

Without complete, tamper-resistant audit trails, organizations lose the ability to investigate incidents, attribute malicious actions, and understand the scope of compromises. This can manifest in various forms, including but not limited to:

- Inability to detect unauthorized modifications to build or deployment processes
- Attackers covering their tracks by modifying or deleting log entries
- Inconsistent or missing timestamps that make forensic reconstruction impossible
- Compliance violations due to inadequate audit capabilities
- Delayed incident response because the scope of a breach cannot be determined

### What are we going to do about it?

1. Make sure all important events in your build, delivery, and deployment processes are logged, including who triggered them, what changed, and when.
2. Store logs somewhere separate that users cannot modify or delete, such as an append-only log store.
3. Use synchronized time sources so that log entries have accurate, consistent timestamps.
5. Periodically check your audit logs for anomalies and gaps. Missing entries can be as telling as suspicious ones.
6. Make sure logs are kept long enough to be useful when something goes wrong. Your organization should have guidelines that recommend or mandate a specific retention period.

For detailed advice on how to mitigate threats related to the card, see the [OWASP SAMM and OWASP DSOMM](#mapping 'OWASP SAMM and OWASP DSOMM requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP SAMM](https://github.com/owaspsamm/core/tree/develop/model/activities) and [OWASP DSOMM](https://dsomm.owasp.org/mapping) documentation.

## Reading the mappings
Mappings use identifiers from [OWASP SAMM](https://owaspsamm.org/model/) and [OWASP DSOMM](https://dsomm.owasp.org/mapping).

SAMM identifiers specify a [Business Function, Security Practice and Stream](https://owaspsamm.org/about/). For example, O-IM-A breaks down as **O**perations - **I**ncident **M**anagement - [Stream **A** (Incident Detection)](https://owaspsamm.org/model/operations/incident-management/stream-a/).

DSOMM identifiers specify a [Dimension and Sub-Dimension](https://dsomm.owasp.org/usage/). For example, IG-L breaks down as **I**nformation **G**athering - **L**ogging. A Sub-Dimension groups multiple related activities, and is used here because the activities as a group correspond to the card's scope.