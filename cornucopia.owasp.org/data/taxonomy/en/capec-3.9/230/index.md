# CAPEC™ 230: Serialized Data with Nested Payloads

## Description

Applications often need to transform data in and out of a data format (e.g., XML and YAML) by using a parser. It may be possible for an adversary to inject data that may have an adverse effect on the parser when it is being processed. Many data format languages allow the definition of macro-like structures that can be used to simplify the creation of complex structures. By nesting these structures, causing the data to be repeatedly substituted, an adversary can cause the parser to consume more resources while processing, causing excessive memory consumption and CPU utilization.

Source: [CAPEC™ 230](https://capec.mitre.org/data/definitions/230.html)

