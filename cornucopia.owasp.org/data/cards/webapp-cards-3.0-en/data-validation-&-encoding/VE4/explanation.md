## Scenario: Dave’s Contextual Manipulation

Imagine a situation where Dave, exploiting a security loophole, inputs malicious field names or data. This occurs because the system fails to check these inputs within the context of the current user and process. Here's how he does it:

1. **Malicious Field Names**: Dave submits field names that are either unrecognized or inappropriate for the current context.

2. **Inappropriate Data Context**: The data entered by Dave is harmful or irrelevant in the specific context of the ongoing process or user's role.

### Example

Dave attacks by altering a web form field. He changes a hidden field named 'user_role' from 'user' to 'admin'. The system, lacking proper contextual validation, mistakenly grants Dave administrative privileges based on this manipulated input, giving him access to sensitive areas of the system.

## Threat Modeling

### STRIDE

The primary STRIDE category for being able to “inputs malicious field names or data” is **Tampering**, but if Dave can change the `user_role` from user to admin, than that lets him obtain higher rights than he should — that is the textbook definition of **elevation of privilege**. The root cause would be missing contextual validation/authorization, so manipulated input is treated as authoritative and results in increased privileges.

### What can go wrong?

This form of attack can lead to unauthorized access, data breaches, and potentially full system compromise.

Malicious data can be introduced voluntarily (as part of an attack) or involuntarily (e.g. XSS). Some input checks should be dependent upon the function or user's context (e.g. the data is valid for one user but not another). There are many alternatives to this kind of attack:

1. Tampering request types, URLs, cookies, session identifiers, fields or values that are not validated.
2. Adding, removing or duplicating request fields or values to exploit code behaviour (e.g. mass parameter assignment, parameter pollution, passing partial authentication data).
3. Sending requests that are processed independently of the user activities (stage, amount of requests, privileges).
4. Fuzzing a file input.

Depending of the target of the attack, the impact of these type of threats varies widely:

1. Information disclosure (error logs, system responses, etc.).
2. Operations tampering (SQLi, eShoplifting).
3. Denial of Service.
4. Privilege escalations
5. Code execution.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Implement strict contextual validation for all data inputs, particularly focusing on user roles and process stages.
2. Continually update and refine validation mechanisms to address new and evolving security threats.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
