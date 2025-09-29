## Scenario: Mwengu’s Untraceable Actions Due to Inadequate Logging and Auditing

Imagine a scenario where Mwengu’s actions within an application cannot be investigated because of insufficient logging and auditing practices. This situation arises from:

1. **Lack of Accurately Time-Stamped Security Event Records:** The application does not maintain a detailed, time-stamped log of security events.

2. **Incomplete Audit Trails:** There is no comprehensive audit trail capturing all user actions.

3. **Tamperable Logs:** Mwengu has the ability to alter or delete logs, making his actions untraceable.

4. **Absence of Centralized Logging:** The system lacks a centralized logging service, leading to fragmented or missing records.

### Example

Mwengu accesses an application that lacks adequate security logging. He performs unauthorized actions, but the application does not record these events with accurate timestamps, nor does it maintain a complete audit trail. Furthermore, due to his advanced access, Mwengu can alter and delete logs to cover his tracks. The absence of centralized logging means there is no single source of truth for investigating Mwengu’s activities, making it challenging to trace his actions or understand their impact.

## Threat Modeling

### STRIDE

The STRIDE category applicable here is **Repudiation**.

**Repudiation** occurs when actions cannot be traced back to the responsible party, typically due to missing or inadequate logging, auditing, or accountability mechanisms.

### What can go wrong?

Inadequate logging and auditing can lead to significant gaps in security oversight, hindering the ability to detect, investigate, and respond to unauthorized activities.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement comprehensive logging of all security-relevant events with accurate time-stamping.
2. Ensure that audit trails are complete, immutable, and protected from unauthorized access and modification.
3. Establish a centralized logging system to consolidate logs from various sources for easier monitoring and analysis.
4. Regularly review and update logging and auditing mechanisms to ensure they capture all necessary information and are secure against tampering.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
