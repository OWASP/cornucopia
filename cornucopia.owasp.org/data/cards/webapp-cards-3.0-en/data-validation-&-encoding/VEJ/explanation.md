## Scenario: Toby’s Control Over Validation and Encoding

Picture a scenario where Toby gains control over crucial aspects of the system’s security - specifically, input validation, output validation, and output encoding routines. This allows him to manipulate these processes:

1. **Control Over Input Validation:** Toby can manipulate or bypass checks on data entering the system.

2. **Influence on Output Validation:** He has the ability to alter or disable validation of data before it's presented or used.

3. **Manipulation of Output Encoding Routines:** Toby can modify how data is encoded before it’s sent to users or other systems, potentially disabling vital security measures.

### Example

Toby exploits his control by disabling certain input validation checks on a form that accepts user data. For instance, he allows special characters or script inputs that are usually blocked. This enables him to insert malicious scripts or commands, which are then executed by the system or other users, leading to vulnerabilities like Cross-Site Scripting (XSS) or command injections.

## Threat Modeling

### STRIDE

Toby is modifying or disabling the code/routines that enforce validation/encoding — that’s an integrity attack which alters the system processes or data so that malicious input is accepted. In STRIDE, that maps directly to **Tampering**, but the consequences of that tampering (XSS, RCE, auth bypass) may map to other STRIDE categories such as Elevation of Privilege or Information Disclosure, so treat those as secondary impacts.

### What can go wrong?

Such control over validation and encoding routines can lead to a wide array of security issues, including data corruption, unauthorized access, and execution of harmful scripts.

Validation and encoding are sometimes undertaken in client applications or external sources that interact with the system. This is a bad practice, as external sources are usually more vulnerable to attacks, can be spoofed and are generally less accountable for malicious behavior. An attacker can try to bypass these routines using non-controlled unexpected behavior:

1. Modifying/deleting code
2. Generating unexpected handcrafted requests
3. Use an automated exploring tool (web crawler) to get information about the file structure and then try to access well known resource locations
4. Abusing an ill-defined zone of trust
5. Modifying data between the client application and the server (e.g. Trojan, modification in transit)
6. XSS

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

In general, all validation and encoding routines should be on the server-side using robust, tested and protected routines.

1. Implement strict access controls and monitoring to prevent unauthorized changes to validation and encoding routines.
2. Regularly review and audit these processes to ensure they haven't been tampered with.
3. Establish robust checks and balances within the development and deployment processes to detect any unauthorized modifications.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
