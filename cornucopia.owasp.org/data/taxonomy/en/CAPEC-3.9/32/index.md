# CAPEC™ 32: XSS Through HTTP Query Strings

## Description

An adversary embeds malicious script code in the parameters of an HTTP query string and convinces a victim to submit the HTTP request that contains the query string to a vulnerable web application. The web application then procedes to use the values parameters without properly validation them first and generates the HTML code that will be executed by the victim's browser.

Source: [CAPEC™ 32](https://capec.mitre.org/data/definitions/32.html)

