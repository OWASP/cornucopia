Malicious data can be introduced voluntarily (as part of an attack) or involuntarily (e.g. XSS). Some input checks should be dependent upon the function or user's context (e.g. the data is valid for one user but not another). There are many alternatives to this kind of attack:

Tampering request types, URLs, cookies, session identifiers, fields or values that are not validated.
Adding, removing or duplicating request fields or values to exploit code behaviour (e.g. mass parameter assignment, parameter pollution, passing partial authentication data).
Sending requests that are processed independently of the user activities (stage, amount of requests, privileges).
Fuzzing a file input.
Depending of the target of the attack, the results of this type of input varies widely:

Information disclosure (error logs, system responses, etc.).
Operations tampering (SQLi, eShoplifting).
Denial of Service.
Spoofing.
Code execution.
NB: This card relates to context-specific input validation. See VE 3 for the similar generic input validation checks.
