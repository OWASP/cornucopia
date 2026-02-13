When object persistence is used to store sensitive information on a mobile device, the integrity and confidentiality of that data must be guaranteed. Serialized objects, JSON files, ORM databases, and other persistence mechanisms can be manipulated on rooted or jailbroken devices or via runtime instrumentation.



Sensitive data stored locally should be encrypted and protected with an HMAC or digital signature. The integrity of the data must always be verified before it is processed or trusted. Cryptographic keys must be securely stored using platform-provided secure storage mechanisms such as Android Keystore or iOS Keychain.



Applications should never rely solely on locally stored authorization flags or business logic indicators without validating their authenticity and integrity.



