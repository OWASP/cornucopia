# CAPEC™ 301: TCP Connect Scan

## Description

An adversary uses full TCP connection attempts to determine if a port is open on the target system. The scanning process involves completing a 'three-way handshake' with a remote port, and reports the port as closed if the full handshake cannot be established. An advantage of TCP connect scanning is that it works against any TCP/IP stack.

Source: [CAPEC™ 301](https://capec.mitre.org/data/definitions/301.html)

