# CAPEC™ 33: HTTP Request Smuggling

## Description

{'p': [{'__prefix': 'xhtml', '__text': 'An adversary abuses the flexibility and discrepancies in the parsing and interpretation of HTTP Request messages using various HTTP headers, request-line and body parameters as well as message sizes (denoted by the end of message signaled by a given HTTP header) by different intermediary HTTP agents (e.g., load balancer, reverse proxy, web caching proxies, application firewalls, etc.) to secretly send unauthorized and malicious HTTP requests to a back-end HTTP agent (e.g., web server).'}, {'__prefix': 'xhtml', '__text': 'See CanPrecede relationships for possible consequences.'}]}

Source: [CAPEC™ 33](https://capec.mitre.org/data/definitions/33.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [4.2.1](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.1), [4.2.2](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.2), [4.2.3](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.3), [4.2.4](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.4)
