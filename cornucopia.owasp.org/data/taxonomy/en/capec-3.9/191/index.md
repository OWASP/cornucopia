# CAPEC™ 191: Read Sensitive Constants Within an Executable

## Description

{'p': {'__prefix': 'xhtml', '__text': 'An adversary engages in activities to discover any sensitive constants present within the compiled code of an executable. These constants may include literal ASCII strings within the file itself, or possibly strings hard-coded into particular routines that can be revealed by code refactoring methods including static and dynamic analysis.'}}

Source: [CAPEC™ 191](https://capec.mitre.org/data/definitions/191.html)

## Related ASVS Requirements

ASVS (5.0): [13.3.1](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.1), [13.4.7](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.7)
