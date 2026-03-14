If object persistence mechanisms are used to store sensitive information locally on a mobile device, proper protection mechanisms must be applied.



Serialized objects (e.g., Serializable, Parcelable, JSON, ORM-backed models) may be modified by attackers on rooted or jailbroken devices, or through runtime instrumentation tools such as Frida or objection.



To mitigate tampering risks:



\- Encrypt sensitive data before storing it locally.

\- Protect serialized objects using HMAC or digital signatures and verify integrity before use.

\- Store cryptographic keys securely using hardware-backed keystore (Android) or Keychain (iOS).

\- Avoid relying on locally stored authorization flags without server-side validation.

\- Validate all deserialized data before processing it.

\- Avoid reflection-based persistence mechanisms in high-risk applications.

\- Disable unnecessary logging of serialized or sensitive objects.



Failure to protect locally persisted objects may result in privilege escalation, business logic manipulation, or unauthorized access to protected functionality.



