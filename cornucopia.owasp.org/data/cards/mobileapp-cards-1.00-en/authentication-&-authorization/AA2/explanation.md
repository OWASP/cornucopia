### Scenario: Jie sign into Choi's mobile app undetected. 
 
Consider a scenario where Jie and Choi live together. Jie and Choi, like all couples, keep secrets from each other, like what they spend their money on. It is not our job to help Jie and Choi with their relationship issues, but it is our job to keep the secrets they store on their mobile phone confidential. We therefore need to help them by ensuring that they authenticate before accessing these secrets. 
 
There are various ways that Jie may get access to Choi's secrets. 
 
1. If Choi's mobile is left unattended and unlocked, Jie may be able to access his app secrets if the unlocked key is not used before opening Choi's mobile application. 
 
2. If Jie has been shoulder surfing when Choi used his mobile, he may know his pin. Even if Choi uses a different pin for his sensitive mobile apps that Jie doesn't have, given that Jie is a north korean spy and hacker, he could extract and decrypt Choi's data as long as the unlocked key not is used during sensitive operations like when decrypting local storage or when decrypting or signing a message before sending or receiving it from a remote endpoint. 
 
3. If Choi has left his phone unlocked then Jie could steal back the money that he paid Choi for the "Bob Dylan concert" if he isn't required to re-authenticate before transferring the money back to him. 
 
### Example: 
 
Choi really wanted to pay his student loan, but he also really needed to go to the bathroom. Sadly, he forgot to lock his phone, leaving the screen bright and tempting on the table for Jie. Jie really would like to know whether it is true that Choi didn't have any money and therefore had to borrow them from him. As Jie opens Chois banking app, he is able to do so without using pin or biometrics, effectively bypassing authentication. There, clear as day, Jie finds all of Chois bank transactions and reads that Choi did have enough money, it's just that he really wanted to attend this really expensive Bob Dylan concert as well. Oh boy, is Choi going to hear it. 
 
### Risks:  
 
If the unlock key is not used or it's not confirmed that the unlocked key has been used, then the mobile application may be vulnerable to local authentication bypass. This type of vulnerability can be exploited by a controlling partner, a spy or a thief to get access to sensitive information. Effectively resulting in a data breach. 
 
### Mitigation: 
 
 - Make sure the unlocked key is used during sensitive operations by configuring the app with the required flags needed for enforcing authentication before using the keychain or key storage. 
 - Limit the amount of time for which the user has been authorized to use a certain key after the user has successfully authenticated. 
 - Confirm that the unlocked key is used before contextual state changes like when changing state from running in the background to running in the foreground. Alternatively enforce re-authentication against a remote endpoint. 
 - Confirm that the unlocked key is used before confirming sensitive operations within the app like when changing the user's email, password, pin or phone number. Alternatively enforce re-authentication against a remote endpoint. 
