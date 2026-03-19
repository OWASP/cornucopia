# CAPEC™ 101: Server Side Include (SSI) Injection

## Description

An attacker can use Server Side Include (SSI) Injection to send code to a web application that then gets executed by the web server. Doing so enables the attacker to achieve similar results to Cross Site Scripting, viz., arbitrary code execution and information disclosure, albeit on a more limited scale, since the SSI directives are nowhere near as powerful as a full-fledged scripting language. Nonetheless, the attacker can conveniently gain access to sensitive files, such as password files, and execute shell commands.

Source: [CAPEC™ 101](https://capec.mitre.org/data/definitions/101.html)

