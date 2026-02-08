# CAPEC™ 67: String Format Overflow in syslog()

## Description

This attack targets applications and software that uses the syslog() function insecurely. If an application does not explicitely use a format string parameter in a call to syslog(), user input can be placed in the format string parameter leading to a format string injection attack. Adversaries can then inject malicious format string commands into the function call leading to a buffer overflow. There are many reported software vulnerabilities with the root cause being a misuse of the syslog() function.

Source: [CAPEC™ 67](https://capec.mitre.org/data/definitions/67.html)

