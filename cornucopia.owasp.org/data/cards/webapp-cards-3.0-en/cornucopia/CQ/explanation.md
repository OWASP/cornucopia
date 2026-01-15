## Scenario: Jim’s Undetected Malicious Activities

Imagine a situation where Jim undertakes malicious or abnormal actions within an application, which go undetected and unaddressed in real-time. This lack of detection and response arises from:

1. **Inadequate Real-Time Monitoring:** The application lacks mechanisms to monitor and identify abnormal or malicious activities as they occur.

2. **Lack of Responsive Measures:** Even if malicious actions are identified, the application does not have an immediate response mechanism to mitigate or halt these actions.

### Example

Jim exploits an online banking application, performing actions that deviate significantly from normal user behavior, such as attempting to access multiple accounts in quick succession. The application, however, does not have real-time monitoring capabilities to flag these activities as suspicious. Moreover, even as Jim’s actions continue, there is no automated response, such as temporarily suspending the account or alerting system administrators, allowing him to probe the system further and exploit vulnerabilities without immediate interference.

## Threat Modeling

### STRIDE

The STRIDE category applicable here is **Repudiation**.

Jim can perform malicious actions without the system detecting or responding in real time.
The key issue is that the system cannot reliably track or attribute actions as they happen, which aligns with **Repudiation** — the inability to prove who performed a given action.
Lack of monitoring and automated response means there’s no immediate accountability or enforcement, which is central to repudiation concerns.

### What can go wrong?

The inability to detect and respond to malicious activities in real-time can lead to extended unauthorized access, data breaches, and significant exploitation of system vulnerabilities.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Implement real-time monitoring tools to detect abnormal or malicious activities as they occur.
2. Develop responsive measures that can automatically react to potential threats, such as account locks, alerts, and triggering additional authentication processes.
3. Regularly update and test the system’s monitoring and response capabilities to ensure they effectively identify and counteract emerging threats.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
