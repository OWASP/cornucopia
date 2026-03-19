# CAPEC™ 293: Traceroute Route Enumeration

## Description

An adversary uses a traceroute utility to map out the route which data flows through the network in route to a target destination. Tracerouting can allow the adversary to construct a working topology of systems and routers by listing the systems through which data passes through on their way to the targeted machine. This attack can return varied results depending upon the type of traceroute that is performed. Traceroute works by sending packets to a target while incrementing the Time-to-Live field in the packet header. As the packet traverses each hop along its way to the destination, its TTL expires generating an ICMP diagnostic message that identifies where the packet expired. Traditional techniques for tracerouting involved the use of ICMP and UDP, but as more firewalls began to filter ingress ICMP, methods of traceroute using TCP were developed.

Source: [CAPEC™ 293](https://capec.mitre.org/data/definitions/293.html)

