Ensuring that the app and its cryptographic keys are accessible only under strict conditions, such as when the device is unlocked by an authenticated user, within secure application contexts, or for limited periods of time, is critical to maintaining the confidentiality and integrity of encrypted data.
 
Make sure the unlocked key is used during sensitive operations. For example when decrypting local storage or when decrypting or signing a message before sending or receiving it from a remote endpoint. You may want to re-authenticate before contextual state changes like when changing state from running in the background to running in the foreground or changing the user's email, password, pin or phone number. Otherwise, the application may be vulnerable to a local authentication bypass. 
 
