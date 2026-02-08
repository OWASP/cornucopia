# CAPEC™ 229: Serialized Data Parameter Blowup

## Description

This attack exploits certain serialized data parsers (e.g., XML, YAML, etc.) which manage data in an inefficient manner. The attacker crafts an serialized data file with multiple configuration parameters in the same dataset. In a vulnerable parser, this results in a denial of service condition where CPU resources are exhausted because of the parsing algorithm. The weakness being exploited is tied to parser implementation and not language specific.

Source: [CAPEC™ 229](https://capec.mitre.org/data/definitions/229.html)

