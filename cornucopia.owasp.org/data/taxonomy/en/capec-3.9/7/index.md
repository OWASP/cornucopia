# CAPEC™ 7: Blind SQL Injection

## Description

Blind SQL Injection results from an insufficient mitigation for SQL Injection. Although suppressing database error messages are considered best practice, the suppression alone is not sufficient to prevent SQL Injection. Blind SQL Injection is a form of SQL Injection that overcomes the lack of error messages. Without the error messages that facilitate SQL Injection, the adversary constructs input strings that probe the target through simple Boolean SQL expressions. The adversary can determine if the syntax and structure of the injection was successful based on whether the query was executed or not. Applied iteratively, the adversary determines how and where the target is vulnerable to SQL Injection.

Source: [CAPEC™ 7](https://capec.mitre.org/data/definitions/7.html)

