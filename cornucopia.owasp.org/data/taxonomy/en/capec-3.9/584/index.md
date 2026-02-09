# CAPEC™ 584: BGP Route Disabling

## Description

An adversary suppresses the Border Gateway Protocol (BGP) advertisement for a route so as to render the underlying network inaccessible. The BGP protocol helps traffic move throughout the Internet by selecting the most efficient route between Autonomous Systems (AS), or routing domains. BGP is the basis for interdomain routing infrastructure, providing connections between these ASs. By suppressing the intended AS routing advertisements and/or forcing less effective routes for traffic to ASs, the adversary can deny availability for the target network.

Source: [CAPEC™ 584](https://capec.mitre.org/data/definitions/584.html)

