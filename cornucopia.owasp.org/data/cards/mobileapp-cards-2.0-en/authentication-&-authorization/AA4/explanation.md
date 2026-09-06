## Scenario: Jie signs into Choi's mobile app without using the “unlocked key”. 

Consider a scenario where Jie and Choi live together. Jie and Choi, like all couples, keep secrets from each other, such as what they spend their money on. It is not our job to help Jie and Choi with their relationship issues, but it is our job to keep the secrets they store on their mobile phones confidential. We therefore need to help them by ensuring that they authenticate before accessing these secrets.
 
There are various ways that Jie may get access to Choi's secrets. 
 
1. If Choi's mobile is left unattended and unlocked, Jie may be able to access the secrets in his apps if the unlocked key is not used before opening Choi's mobile application.
 
2. If Jie has been shoulder surfing when Choi used his mobile, he may know his PIN. Even if Choi uses a different PIN for his sensitive mobile apps that Jie does not have, given that Jie is a North Korean spy and hacker, he could extract and decrypt Choi's data as long as the unlocked key is not used during sensitive operations, such as decrypting local storage or decrypting or signing a message before sending it to or receiving it from a remote endpoint.
 
3. If Choi has left his phone unlocked, then Jie could steal back the money that he paid Choi for the "Bob Dylan concert" if he is not required to re-authenticate before transferring the money back to him.
 
### Example
 
Choi really wanted to pay his student loan, but he also really needed to go to the bathroom. Sadly, he forgot to lock his phone, leaving the screen bright and tempting on the table for Jie. Jie really wants to know whether it is true that Choi did not have any money and therefore had to borrow money from him. As Jie opens Choi's banking app, he is able to do so without using a PIN or biometrics, effectively bypassing authentication. There, clear as day, Jie finds all of Choi's bank transactions and reads that Choi did have enough money; he just wanted to attend the expensive Bob Dylan concert as well. Oh boy, is Choi going to hear it.
 
## Threat Modeling

### STRIDE

This scenario falls under the **Spoofing** category in STRIDE.
Jie is successfully masquerading as Choi to gain unauthorized access to the app. By bypassing or avoiding authentication, the system fails to verify the user's true identity, allowing Jie to act with Choi's privileges and compromise his data confidentiality.

### What can go wrong? 
 
If the unlock key is not used or it has not been confirmed that the unlocked key has been used, then the mobile application may be vulnerable to local authentication bypass. This type of vulnerability can be exploited by a controlling partner, a spy, or a thief to gain access to sensitive information, effectively resulting in a data breach.
 
### What are we going to do about it?
 
 - Make sure the unlocked key is used during sensitive operations by configuring the app with the flags required to enforce authentication before using the keychain or key storage.
 - Limit the amount of time for which the user is authorized to use a certain key after successfully authenticating.
 - Confirm that the unlocked key is used before contextual state changes, such as changing state from running in the background to running in the foreground. Alternatively, enforce re-authentication against a remote endpoint.
 - Confirm that the unlocked key is used before confirming sensitive operations within the app, such as changing the user's email, password, PIN, or phone number. Alternatively, enforce re-authentication against a remote endpoint.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.