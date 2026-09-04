## Scenario: Aatif can influence or alter authentication controls and can therefore bypass them

### Example

Aatif helps install a smart gate opener app for a customer so that the owner can open the gate to their property using their face or fingerprint. What the customer does not know is that the app verifies the biometric locally and sends a simple, unsigned local command to the gate stating `auth_status=success` and `time_of_entry=(time of entry)`. Having performed some "Wiresharking" during the installation, Aatif knows exactly which request to send to the gate. At night, Aatif replays the command, changing the `time_of_entry` parameter to the current time and sending it to the gate's receiver, thereby bypassing the phone's biometric control entirely.

## Threat Modeling

### STRIDE

This scenario covers four of the STRIDE categories: **Spoofing**, **Tampering**, **Repudiation**, and **Information Disclosure**.
By sending the command, Aatif successfully spoofs the identity of the authorized property owner to gain entry.
He intercepts the original packet and tampers with the time_of_entry parameter, changing it to the current time so the receiver accepts it as a fresh request.
Because the gate blindly trusts the `auth_status=success` command, its internal logs will record that the legitimate owner opened the gate at that specific time. If a theft occurs, the owner can rightfully deny being there, but the system logs will falsely incriminate them, creating a repudiation issue.
The app transmits highly sensitive authorization commands in plain text (or weak encryption) over the local network.


### What can go wrong?

Because Aatif can influence or alter authentication controls and bypass them, the app lets an attacker break into the property without proper authorization and without being detected.

### What are we going to do about it?

Make authentication checks and their configuration tamper-resistant: use platform-protected keys, verify server-issued challenges, reject altered state, and fail closed when a hook or modified verifier is detected; exercise both static references and runtime behavior. Also make sure the app communicates over a secure channel when doing sensitive operations.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.
