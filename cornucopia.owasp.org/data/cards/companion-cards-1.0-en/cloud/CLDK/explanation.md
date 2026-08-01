## Scenario: Daniele's Compromise of the Cloud Root Account

Daniele gains access to the cloud root or break-glass account and achieves irreversible control over billing, identity management, and all recovery mechanisms. This occurs because:

1. **Root Account Used for Day-to-Day Operations:** The root account's credentials are used for routine administrative tasks rather than being locked away and reserved exclusively for break-glass scenarios, increasing the frequency and surface area of credential exposure.

2. **No Multi-Factor Authentication on the Root Account:** The root account is not protected by multi-factor authentication, meaning a username and password alone are sufficient to gain full, unrestricted control of the entire cloud account.

3. **Root Credentials Stored Insecurely:** Root access keys or passwords are stored in shared team password managers, email inboxes, or other locations accessible to a broader group of people than intended.

### Example

Daniele targets a cloud administrator at a technology company through a spear-phishing campaign, crafting a convincing message that mimics the cloud provider's billing team. The administrator, who has root credentials stored in a shared team password manager, clicks through a credential harvesting page and enters their username and password. Because the root account has no multi-factor authentication configured, Daniele immediately authenticates as root. He begins by creating a new administrator user with long-lived access keys — establishing persistence before any response can be mounted. He then modifies the account's contact information to redirect alerts, deletes audit logs to remove evidence of the intrusion, and changes the root email address and recovery phone number. When the company attempts to recover the account through the standard process, they find that Daniele has locked them out of every recovery path.

## Threat Modeling

### STRIDE

**Primary: Spoofing**

Daniele spoofs his identity as a legitimate administrator by harvesting credentials through a phishing email that mimics the cloud provider's billing team. Once authenticated with stolen credentials, he is trusted by the system as the root account holder. The lack of multi-factor authentication means the system cannot distinguish between the legitimate administrator and the attacker using the same credentials.

### What can go wrong?

Compromise of the cloud root account is the most severe cloud security incident possible. The root account has permissions that cannot be restricted by any IAM policy, it can delete all other administrators, disable security controls for all users, close the account, access all data, and circumvent every safeguard. Recovery from a root account takeover where the attacker has changed recovery credentials may require a lengthy engagement with the cloud provider's support teams and may result in permanent data loss. The attacker can also weaponize billing by spinning up expensive resources, resulting in significant financial damage.

### What are we going to do about it?

Protect the root account with the strictest possible controls and eliminate its use for any routine operations.

1. Force hardware multi-factor authentication (e.g., a FIDO2 security key) on the root account and store the physical device in a physically secure location with documented break-glass procedures.
2. Never create root access keys; use IAM users or roles with appropriate permissions for all routine administrative tasks instead.
3. Store root credentials and recovery codes in a dedicated, hardware-protected secrets store — not in a shared team password manager, email inbox, or any system accessible to more than one or two individuals.