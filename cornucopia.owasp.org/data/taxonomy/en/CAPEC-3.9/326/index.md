# CAPEC™ 326: TCP Initial Window Size Probe

## Description

This OS fingerprinting probe checks the initial TCP Window size. TCP stacks limit the range of sequence numbers allowable within a session to maintain the "connected" state within TCP protocol logic. The initial window size specifies a range of acceptable sequence numbers that will qualify as a response to an ACK packet within a session. Various operating systems use different Initial window sizes. The initial window size can be sampled by establishing an ordinary TCP connection.

Source: [CAPEC™ 326](https://capec.mitre.org/data/definitions/326.html)

