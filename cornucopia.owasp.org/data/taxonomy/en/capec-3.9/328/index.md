# CAPEC™ 328: TCP 'RST' Flag Checksum Probe

## Description

This OS fingerprinting probe performs a checksum on any ASCII data contained within the data portion or a RST packet. Some operating systems will report a human-readable text message in the payload of a 'RST' (reset) packet when specific types of connection errors occur. RFC 1122 allows text payloads within reset packets but not all operating systems or routers implement this functionality.

Source: [CAPEC™ 328](https://capec.mitre.org/data/definitions/328.html)

