## Scenario: Anant can perform sensitive operations without step-up or re-authentication because authentication requirements have not taken into account risk related to transactions or contextual changes

### Example

Anant brother, a notorious casanova, keeps track of the names and phone number of all the girls that he dates in a black note book that he keeps in a consumer safe in his room. After a falling-out, Anant decides he wants to see his brother's secrets notes so that he can make prank calls to some of his brother's girlfriends. The safe uses a mobile app to lock and unlock the door. In a moment of unawareness, while going to the kitchen for some snacks, Anant grabs his brother's unlocked phone, points it towards the ceiling (where his brother's room is), and pushes the unlock button. The safe opens and his brothers secret black book, aren't that secret anymore.

## Threat Modeling

### STRIDE

This scenario falls under the **Spoofing**, **Elevation of Privilege** and **Information Disclosure** categories of STRIDE. The app used by the safe performs sensitive actions without step-up or re-authentication allowing Anant to easily access his brother's safe by pushing a button.
Anant performs **Spoofing** due to missing step-up or re-authentication. That allows him to elevate his own privileges (**Elevation of Privilege**) by opening his brothers safe, and accessing his brother's secret black book, leading to **Information Disclosure**.

### What can go wrong?

**Missing step-up or re-authentication:** If sensitive actions can be submitted without aditional step-up or re-authentication, these actions may get exploited while the user is distracted.

**Insecure Storage:** If the key for encryption of sensitive data stored on the mobile phone can be accessed without a successful biometric or PIN verification, bypassing the apps authentication screen grants immediate access to sensitive data.

### What are we going to do about it?

**Android Keystore / iOS Keychain:** Use cryptographic keys that mandate user authentication (e.g., `setUserAuthenticationRequired(true)`).

**Crypto-Binding:** Ensure the sensitive data can only be decrypted using the key that is released *only* after a successful biometric or PIN verification.

**Step-up or Re-authentication:** Ensure senstive transactions are protected by an extra authentication step before the transaction is executed.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.