# CAPEC™ 256: SOAP Array Overflow

## Description

An attacker sends a SOAP request with an array whose actual length exceeds the length indicated in the request. If the server processing the transmission naively trusts the specified size, then an attacker can intentionally understate the size of the array, possibly resulting in a buffer overflow if the server attempts to read the entire data set into the memory it allocated for a smaller array.

Source: [CAPEC™ 256](https://capec.mitre.org/data/definitions/256.html)

