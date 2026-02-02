# CAPEC™ 221: Data Serialization External Entities Blowup

## Description

This attack takes advantage of the entity replacement property of certain data serialization languages (e.g., XML, YAML, etc.) where the value of the replacement is a URI. A well-crafted file could have the entity refer to a URI that consumes a large amount of resources to create a denial of service condition. This can cause the system to either freeze, crash, or execute arbitrary code depending on the URI.

Source: [CAPEC™ 221](https://capec.mitre.org/data/definitions/221.html)

