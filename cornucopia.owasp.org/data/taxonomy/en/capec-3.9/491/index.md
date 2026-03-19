# CAPEC™ 491: Quadratic Data Expansion

## Description

An adversary exploits macro-like substitution to cause a denial of service situation due to excessive memory being allocated to fully expand the data. The result of this denial of service could cause the application to freeze or crash. This involves defining a very large entity and using it multiple times in a single entity substitution. CAPEC-197 is a similar attack pattern, but it is easier to discover and defend against. This attack pattern does not perform multi-level substitution and therefore does not obviously appear to consume extensive resources.

Source: [CAPEC™ 491](https://capec.mitre.org/data/definitions/491.html)

