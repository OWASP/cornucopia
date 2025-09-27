## Scenario: Dave’s Contextual Manipulation

Imagine a situation where Dave, exploiting a security loophole, inputs malicious field names or data. This occurs because the system fails to check these inputs within the context of the current user and process. Here's how he does it:

1. **Malicious Field Names**: Dave submits field names that are either unrecognized or inappropriate for the current context.

2. **Inappropriate Data Context**: The data entered by Dave is harmful or irrelevant in the specific context of the ongoing process or user's role.

### Example

Dave attacks by altering a web form field. He changes a hidden field named 'user_role' from 'user' to 'admin'. The system, lacking proper contextual validation, mistakenly grants Dave administrative privileges based on this manipulated input, giving him access to sensitive areas of the system.

## Threat Modeling

### STRIDE

The primary STRIDE category for being able to “inputs malicious field names or data” is **Tampering**, but if Dave can change the `user_role` from user to admin, than that lets him obtain higher rights than he should — that is the textbook definition of **elevation of privilege**. The root cause would be missing contextual validation/authorization, so manipulated input is treated as authoritative and results in increased privileges.

### What can go Wrong?

This form of attack can lead to unauthorized access, data breaches, and potentially full system compromise.

### What are you going to do about it?

1. Implement strict contextual validation for all data inputs, particularly focusing on user roles and process stages.
2. Continually update and refine validation mechanisms to address new and evolving security threats.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
