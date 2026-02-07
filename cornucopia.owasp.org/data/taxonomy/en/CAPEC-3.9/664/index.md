# CAPEC™ 664: Server Side Request Forgery

## Description

{'p': {'__prefix': 'xhtml', '__text': "An adversary exploits improper input validation by submitting maliciously crafted input to a target application running on a server, with the goal of forcing the server to make a request either to itself, to web services running in the server’s internal network, or to external third parties. If successful, the adversary’s request will be made with the server’s privilege level, bypassing its authentication controls. This ultimately allows the adversary to access sensitive data, execute commands on the server’s network, and make external requests with the stolen identity of the server. Server Side Request Forgery attacks differ from Cross Site Request Forgery attacks in that they target the server itself, whereas CSRF attacks exploit an insecure user authentication mechanism to perform unauthorized actions on the user's behalf."}}

Source: [CAPEC™ 664](https://capec.mitre.org/data/definitions/664.html)

## Related ASVS Requirements

ASVS (5.0): [1.3.6](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.6), [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1), [5.3.2](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.2)
