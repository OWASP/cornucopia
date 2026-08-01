## Scenario: Invent your own Data Validation & Encoding threat

If you don’t validate and encode data on input and output, a wide range of vulnerabilities can arise, because untrusted data flows unchecked through the system. 

Bottom line:

- If you don’t validate input, attackers can get data in.
- If you don’t encode output, attackers can get code out.

Both together break the trust boundary between users and your system.

Do you want me to also give you a short checklist of best practices for safe input validation & output encoding (something you could apply directly in design or code reviews)?

## Threat Modeling

### STRIDE

Failing to validate and encode properly doesn’t just hit one STRIDE category — it touches almost all of them, depending on the exploit.

1. Tampering → Data/query manipulation, file/resource changes.
2. Information Disclosure → Error messages, XSS, exposed code.
3. Elevation of Privilege → Injections, file uploads.
4. Spoofing → Auth bypass.
5. Denial of Service → Crashes, resource exhaustion.

### What can go wrong?

#### Input Validation Failures

1. SQL Injection – Attackers inject SQL queries through form fields or parameters to read, modify, or delete database data.
2. Command Injection – Malicious input gets executed by the OS (e.g., ; rm -rf /).
3. LDAP / NoSQL Injection – Attackers manipulate directory or database queries.
4. Buffer Overflows – Unchecked input leads to memory corruption or arbitrary code execution.
5. Authentication/Authorization Bypass – Input manipulation allows skipping login checks.

#### Output Encoding Failures

1. Cross-Site Scripting (XSS) – Malicious scripts injected into web pages execute in users’ browsers.
2. HTTP Response Splitting – Attackers craft headers that manipulate server responses.
3. HTML/JavaScript Injection – Unsafe output enables script execution in web apps.
4. Data Leakage – Sensitive info (like raw database errors) shown directly to users.

#### Combined Risks

1. Privilege Escalation – Malicious payloads manipulate flows to gain higher access.
2. Security Misconfigurations – Unvalidated input might toggle debug features or hidden APIs.
3. Malware Distribution – Attackers upload unvalidated files and trick users into downloading them later.

### What are we going to do about it?

Validate input = stop bad data from entering.
Encode output = stop injected data from executing.
