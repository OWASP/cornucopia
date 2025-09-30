## Key Concept

This card is related to notification of events to users.

## Scenario: James’s Unnoticed Authentication Interference

Consider a scenario where James, a cunning hacker, carries out authentication-related activities, such as password changes, without alerting the real user. He exploits security gaps in the notification and monitoring processes:

1. **Undetected Login Attempts:** James attempts to log in using acquired credentials without triggering any alerts.

2. **Unauthorized Logins:** He successfully logs in with stolen credentials, and the real user remains unaware.

3. **Silent Password Resets:** James resets passwords without the system notifying the legitimate account holder.

### Example

James uses stolen credentials to attempt a password reset on a user’s account. The system, lacking a robust alert mechanism, does not notify the actual user of this reset attempt. James successfully changes the password, gains full access to the account, and the legitimate user remains oblivious until they try to access their account later.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Repudiation**.

James is able to perform authentication-related actions without the legitimate user being aware.
STRIDE’s **Repudiation** threat category is about the ability to perform actions that cannot be traced or denied — essentially a lack of sufficient logging, auditing, or notification.
The absence of alerts/notifications means the legitimate user cannot detect or contest the malicious activity. That is classic repudiation risk. Depending on the context, any of the other categories could be a secondary or related impact.

### What can go wrong?

This kind of vulnerability can lead to unnoticed account takeovers, prolonged unauthorized access, and potentially significant data breaches or identity theft.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement immediate alert systems for any authentication-related activities, especially password resets or changes.
2. Enforce multi-factor authentication, which adds a layer of security and verification before allowing password changes or resets.
3. Regularly review authentication processes to ensure they are secure and notify users of all significant activities.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
