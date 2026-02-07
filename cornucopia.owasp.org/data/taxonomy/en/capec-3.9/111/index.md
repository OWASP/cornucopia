# CAPEC™ 111: JSON Hijacking (aka JavaScript Hijacking)

## Description

An attacker targets a system that uses JavaScript Object Notation (JSON) as a transport mechanism between the client and the server (common in Web 2.0 systems using AJAX) to steal possibly confidential information transmitted from the server back to the client inside the JSON object by taking advantage of the loophole in the browser's Same Origin Policy that does not prohibit JavaScript from one website to be included and executed in the context of another website.

Source: [CAPEC™ 111](https://capec.mitre.org/data/definitions/111.html)

## Related ASVS Requirements

ASVS (5.0): [3.4.3](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.3), [3.4.6](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.6), [3.4.7](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.7)
