# CAPEC™ 228: DTD Injection

## Description

An attacker injects malicious content into an application's DTD in an attempt to produce a negative technical impact. DTDs are used to describe how XML documents are processed. Certain malformed DTDs (for example, those with excessive entity expansion as described in CAPEC 197) can cause the XML parsers that process the DTDs to consume excessive resources resulting in resource depletion.

Source: [CAPEC™ 228](https://capec.mitre.org/data/definitions/228.html)

