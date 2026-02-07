# CAPEC™ 481: Contradictory Destinations in Traffic Routing Schemes

## Description

Adversaries can provide contradictory destinations when sending messages. Traffic is routed in networks using the domain names in various headers available at different levels of the OSI model. In a Content Delivery Network (CDN) multiple domains might be available, and if there are contradictory domain names provided it is possible to route traffic to an inappropriate destination. The technique, called Domain Fronting, involves using different domain names in the SNI field of the TLS header and the Host field of the HTTP header. An alternative technique, called Domainless Fronting, is similar, but the SNI field is left blank.

Source: [CAPEC™ 481](https://capec.mitre.org/data/definitions/481.html)

## Related ASVS Requirements

ASVS (5.0): [13.1.1](/taxonomy/asvs-5.0/13-configuration/01-configuration-documentation#V13.1.1), [13.2.4](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.4), [13.2.5](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.5), [15.3.2](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/03-defensive-coding#V15.3.2)
