# CAPEC™ 271: Schema Poisoning

## Description

An adversary corrupts or modifies the content of a schema for the purpose of undermining the security of the target. Schemas provide the structure and content definitions for resources used by an application. By replacing or modifying a schema, the adversary can affect how the application handles or interprets a resource, often leading to possible denial of service, entering into an unexpected state, or recording incomplete data.

Source: [CAPEC™ 271](https://capec.mitre.org/data/definitions/271.html)

## Related ASVS Requirements

ASVS (5.0): [1.5.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.1), [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2)
