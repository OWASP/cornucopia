### Scenario: Cecilia’s Brute Force and Dictionary Attacks 
Imagine a situation where Cecilia, employing brute force and dictionary attack techniques, targets the authentication system of an application. She takes advantage of: 

1. **No Limit on Login Attempts:** The system does not restrict the number of login attempts, allowing repeated guessing. 

2. **Simplified Attacks Due to Weak Password Policies:** Insufficient complexity, length, and expiration requirements make passwords easier to guess. 

3. **Lack of Re-use Limitations:** The system allows the reuse of old passwords, making it easier for attackers to regain access. 

### Example: 

Cecilia targets an online platform that lacks account lockout policies and has weak password requirements. She uses automated tools to repeatedly attempt logins on various accounts, trying combinations from commonly used passwords and dictionary words. Due to the absence of complexity and length requirements for passwords, and no system to detect or block repeated failed attempts, she eventually succeeds in guessing the correct credentials for several accounts. 

### Risks: 

This type of vulnerability exposes users to account takeover, data breaches, and potentially, the compromise of the entire system. 

### Mitigation: 

- Implement a strict account lockout policy after a certain number of failed login attempts to prevent brute force attacks. 
- Enforce strong password policies, including minimum length, complexity, and expiration requirements. 
- Prohibit the reuse of previous passwords to enhance security against repeated attack attempts. 