# CAPEC™ 203: Manipulate Registry Information

## Description

An adversary exploits a weakness in authorization in order to modify content within a registry (e.g., Windows Registry, Mac plist, application registry). Editing registry information can permit the adversary to hide configuration information or remove indicators of compromise to cover up activity. Many applications utilize registries to store configuration and service information. As such, modification of registry information can affect individual services (affecting billing, authorization, or even allowing for identity spoofing) or the overall configuration of a targeted application. For example, both Java RMI and SOAP use registries to track available services. Changing registry values is sometimes a preliminary step towards completing another attack pattern, but given the long term usage of many registry values, manipulation of registry information could be its own end.

Source: [CAPEC™ 203](https://capec.mitre.org/data/definitions/203.html)

## Related ASVS Requirements

ASVS (5.0): [10.2.3](/taxonomy/asvs-5.0/10-oauth-and-oidc/02-oauth-client#V10.2.3), [13.2.2](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.2), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [8.1.1](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.1)
