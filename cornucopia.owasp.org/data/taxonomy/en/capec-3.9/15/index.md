# CAPEC™ 15: Command Delimiters

## Description

An attack of this type exploits a programs' vulnerabilities that allows an attacker's commands to be concatenated onto a legitimate command with the intent of targeting other resources such as the file system or database. The system that uses a filter or denylist input validation, as opposed to allowlist validation is vulnerable to an attacker who predicts delimiters (or combinations of delimiters) not present in the filter or denylist. As with other injection attacks, the attacker uses the command delimiter payload as an entry point to tunnel through the application and activate additional attacks through SQL queries, shell commands, network scanning, and so on.

Source: [CAPEC™ 15](https://capec.mitre.org/data/definitions/15.html)

