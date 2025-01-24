Without knowing the character encoding accurately, data validation routines could be inadequate. A web application firewall, a web server, an application server, a database server, and other interpreters could each be susceptible, and susceptible in different ways, to malicious character encoding issues.

Common protection techniques include:

Specify proper character sets, such as UTF-8, for all sources of input.
Encode data to a common character set before validating (Canonicalize).
Use system components that support UTF-8 extended character sets and validate data after UTF-8 decoding is completed.
NB: The key concept for this card is encoding.
