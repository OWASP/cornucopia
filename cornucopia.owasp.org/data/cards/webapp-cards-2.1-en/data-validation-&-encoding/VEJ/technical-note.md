Validation and encoding are sometimes undertaken in client applications or external sources that interact with the system. This is a bad practice, as external sources are usually more vulnerable to attacks, can be spoofed and are generally less accountable for malicious behaviour. An attacker can try to bypass these routines using non-controlled unexpected behaviour:

Modifying/deleting code.
Generating unexpected handcrafted requests.
Use an automated exploring tool (web crawler) to get information about the file structure and then try to access well known resource locations.
Abusing an ill-defined zone of trust.
Modifying data between the client application and the server (e.g. Trojan, modification in transit)
XSS.
In general, all validation and encoding routines should be on the server-side using robust, tested and protected routines.

NB: Unlike other cards in this suit, this VE J relates to an attacker being able to change the executing code. This may be due to inadequate source code control, deployment controls or server protection, but is more often a standard feature of client-side code.
