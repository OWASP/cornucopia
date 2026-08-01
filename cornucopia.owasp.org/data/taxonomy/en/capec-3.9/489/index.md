# CAPEC™ 489: SSL Flood

## Description

An adversary may execute a flooding attack using the SSL protocol with the intent to deny legitimate users access to a service by consuming all the available resources on the server side. These attacks take advantage of the asymmetric relationship between the processing power used by the client and the processing power used by the server to create a secure connection. In this manner the attacker can make a large number of HTTPS requests on a low provisioned machine to tie up a disproportionately large number of resources on the server. The clients then continue to keep renegotiating the SSL connection. When multiplied by a large number of attacking machines, this attack can result in a crash or loss of service to legitimate users.

Source: [CAPEC™ 489](https://capec.mitre.org/data/definitions/489.html)

