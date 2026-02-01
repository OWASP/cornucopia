## STRIDE: Tampering

An attacker installs the mobile app and observes how it communicates with the backend service. By intercepting and modifying requests, the attacker changes values such as identifiers, roles, or feature-related parameters sent by the app.

If the backend assumes that these values are trustworthy because they originate from the client, the attacker may be able to access restricted functionality, perform unauthorized actions, or modify data belonging to other users.

This issue commonly arises when security decisions are enforced on the device rather than being validated and authorized on the server.

### What could go wrong?

If requests can be modified without proper server-side validation and authorization, attackers can tamper with application logic, bypass access controls, and manipulate sensitive data in ways not intended by the application design.
