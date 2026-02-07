# CAPEC™ 448: Embed Virus into DLL

## Description

An adversary tampers with a DLL and embeds a computer virus into gaps between legitimate machine instructions. These gaps may be the result of compiler optimizations that pad memory blocks for performance gains. The embedded virus then attempts to infect any machine which interfaces with the product, and possibly steal private data or eavesdrop.

Source: [CAPEC™ 448](https://capec.mitre.org/data/definitions/448.html)

