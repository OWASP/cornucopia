# CAPEC™ 320: TCP Timestamp Probe

## Description

This OS fingerprinting probe examines the remote server's implementation of TCP timestamps. Not all operating systems implement timestamps within the TCP header, but when timestamps are used then this provides the attacker with a means to guess the operating system of the target. The attacker begins by probing any active TCP service in order to get response which contains a TCP timestamp. Different Operating systems update the timestamp value using different intervals. This type of analysis is most accurate when multiple timestamp responses are received and then analyzed. TCP timestamps can be found in the TCP Options field of the TCP header.

Source: [CAPEC™ 320](https://capec.mitre.org/data/definitions/320.html)

