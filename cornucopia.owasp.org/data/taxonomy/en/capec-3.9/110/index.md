# CAPEC™ 110: SQL Injection through SOAP Parameter Tampering

## Description

An attacker modifies the parameters of the SOAP message that is sent from the service consumer to the service provider to initiate a SQL injection attack. On the service provider side, the SOAP message is parsed and parameters are not properly validated before being used to access a database in a way that does not use parameter binding, thus enabling the attacker to control the structure of the executed SQL query. This pattern describes a SQL injection attack with the delivery mechanism being a SOAP message.

Source: [CAPEC™ 110](https://capec.mitre.org/data/definitions/110.html)

