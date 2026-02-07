# CAPEC™ 51: Poison Web Service Registry

## Description

SOA and Web Services often use a registry to perform look up, get schema information, and metadata about services. A poisoned registry can redirect (think phishing for servers) the service requester to a malicious service provider, provide incorrect information in schema or metadata, and delete information about service provider interfaces.

Source: [CAPEC™ 51](https://capec.mitre.org/data/definitions/51.html)

## Related ASVS Requirements

ASVS (5.0): [1.3.6](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.6)
