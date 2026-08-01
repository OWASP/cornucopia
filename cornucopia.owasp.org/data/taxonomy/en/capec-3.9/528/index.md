# CAPEC™ 528: XML Flood

## Description

An adversary may execute a flooding attack using XML messages with the intent to deny legitimate users access to a web service. These attacks are accomplished by sending a large number of XML based requests and letting the service attempt to parse each one. In many cases this type of an attack will result in a XML Denial of Service (XDoS) due to an application becoming unstable, freezing, or crashing.

Source: [CAPEC™ 528](https://capec.mitre.org/data/definitions/528.html)

