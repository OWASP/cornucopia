# CAPEC™ 1: Accessing Functionality Not Properly Constrained by ACLs

## Description

In applications, particularly web applications, access to functionality is mitigated by an authorization framework. This framework maps Access Control Lists (ACLs) to elements of the application's functionality; particularly URL's for web apps. In the case that the administrator failed to specify an ACL for a particular element, an attacker may be able to access it with impunity. An attacker with the ability to access functionality not properly constrained by ACLs can obtain sensitive information and possibly compromise the entire application. Such an attacker can access resources that must be available only to users at a higher privilege level, can access management sections of the application, or can run queries for data that they otherwise not supposed to.

Source: [CAPEC™ 1](https://capec.mitre.org/data/definitions/1.html)

## Related ASVS Requirements

ASVS (5.0): [13.2.2](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.2), [13.3.2](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.2), [14.2.4](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.4), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [8.1.1](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.1), [8.1.4](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.4), [8.2.1](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.1), [8.3.1](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.1), [8.4.1](/taxonomy/asvs-5.0/08-authorization/04-other-authorization-considerations#V8.4.1), [8.4.2](/taxonomy/asvs-5.0/08-authorization/04-other-authorization-considerations#V8.4.2)
