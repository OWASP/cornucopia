# CAPEC™ 493: SOAP Array Blowup

## Description

An adversary may execute an attack on a web service that uses SOAP messages in communication. By sending a very large SOAP array declaration to the web service, the attacker forces the web service to allocate space for the array elements before they are parsed by the XML parser. The attacker message is typically small in size containing a large array declaration of say 1,000,000 elements and a couple of array elements. This attack targets exhaustion of the memory resources of the web service.

Source: [CAPEC™ 493](https://capec.mitre.org/data/definitions/493.html)

