\### Scenario



Abdullah edits reality.



Abdullah recently discovered that rooting his Android phone opens up a whole new world of possibilities. While exploring the app’s internal storage, he notices that user information is stored locally in a serialized object. Conveniently, it contains a flag called “isPremiumUser”.



Abdullah is not a premium user.



Yet.



Using a runtime instrumentation tool, Abdullah hooks into the deserialization process and inspects the stored object. He modifies the value of “isPremiumUser” from false to true before the app finishes loading it.



The app happily trusts the modified object.



Suddenly, Abdullah has access to premium features, administrative controls, and content he never paid for.



All because the app assumed local data had not been altered.



\### Example



Abdullah extracts a locally stored JSON file containing his profile data. He edits the file to change his role from “standard” to “admin” and reinjects it into the application sandbox. When the app starts, it deserializes the object and grants him elevated privileges without verifying its integrity.



The app believed the data. The data believed Abdullah. Security believed in hope.



\### Threat Modeling



\### STRIDE



The situation falls under the Tampering category in the STRIDE threat modeling framework.



Abdullah modifies locally stored serialized data before it is processed by the application. Because the application does not verify integrity or authenticity, the manipulated data alters application behavior and grants unauthorized privileges.



\### What can go wrong?



If sensitive information or authorization state is stored locally without proper protection:



\- Serialized objects may be modified before deserialization  

\- JSON or ORM-backed data may be edited directly on rooted or jailbroken devices  

\- Reflection-based persistence mechanisms may be manipulated  

\- Runtime instrumentation (e.g., Frida) may hook deserialization methods  



This can result in privilege escalation, data manipulation, bypass of business logic, or unauthorized access to sensitive functionality.



\### What are we going to do about it?



\- Encrypt sensitive data before storing it on the device.  

\- Protect stored objects with HMAC or digital signatures and verify integrity before use.  

\- Store cryptographic keys securely (e.g., hardware-backed keystore or keychain).  

\- Avoid trusting locally stored authorization flags without server-side validation.  

\- Validate all deserialized data before processing it.  

\- Avoid reflection-based persistence in high-risk applications.



