## Scenario: Prasad can bypass the centralized authentication and authorization controls because they are not applied comprehensively to all interactions

### Example

Prasad visits a charity book sale at his favorite local bookshop. For this, the shop uses an app where the tablet asks the cashier for a PIN at login but asks nothing of the visiting customer, then leaves the button for the cashier's sales dashboard exposed on every later screen. He taps through the catalog, finds and opens the cashier's sales dashboard, and discovers that the “honor system” comes with a surprisingly generous refund menu, thereby making the charity book sale more charitable than intended.

## Threat Modeling

### STRIDE

This scenario is primarily **Elevation of Privilege** in STRIDE because Prasad can bypass the centralized authentication and authorization controls because they are not applied comprehensively to all interactions. He is not entering the cashier's PIN (**Spoofing**); he is granting himself unauthorized access (**Elevation of Privilege**).

### What can go wrong?

Authentication and authorization controls may be centralized in appearance but missing from individual interactions. An app in which these controls are missing from individual interactions may let a caller reach protected operations after passing a superficial check.
If Prasad can bypass the centralized authentication and authorization controls because they are not being used comprehensively on all interactions, the app could let an attacker bypass the authentication and authorization boundaries and reach data or capabilities that this flow should protect. Attack vectors include:

- Debugging the app at runtime.
- Using dynamic instrumentation.
- Misusing logical flaws.

### What are we going to do about it?

Enforce authentication and authorization at every entry point, not just the main screen: test the release build while debugging and instrumenting it, protect IPC with narrow permissions, and have the server re-check the identity and each sensitive action.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.