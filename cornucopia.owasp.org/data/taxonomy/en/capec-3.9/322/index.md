# CAPEC™ 322: TCP (ISN) Greatest Common Divisor Probe

## Description

This OS fingerprinting probe sends a number of TCP SYN packets to an open port of a remote machine. The Initial Sequence Number (ISN) in each of the SYN/ACK response packets is analyzed to determine the smallest number that the target host uses when incrementing sequence numbers. This information can be useful for identifying an operating system because particular operating systems and versions increment sequence numbers using different values. The result of the analysis is then compared against a database of OS behaviors to determine the OS type and/or version.

Source: [CAPEC™ 322](https://capec.mitre.org/data/definitions/322.html)

