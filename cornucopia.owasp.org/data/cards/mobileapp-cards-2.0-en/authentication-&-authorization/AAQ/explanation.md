## Scenario: Riotaro can bypass authorization controls by exploiting data flows between views, processes, and components to inject commands, manipulate data, or disclose sensitive information

### Example

Riotaro is a disgruntled volunteer backstage at a school play, where a tablet used for lighting and video presentation, belonging to the lead performer, passes scene details through a shared message bus connected to the video projector. He slips a compromising image of the star on stage into the handoff and dutifully rewards the audience with a mythical bonus show.

The receiving component accepts a command merely because it arrived through a neighboring component. Data flowing between views, processes, and services needs authorization and validation at each boundary, or a crafted message can trigger sensitive actions or expose their results.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure**, and **Elevation of Privilege** in STRIDE. Riotaro can bypass authorization controls and elevate his privileges by tampering with data flows between views, processes, and components to inject commands, manipulate data, or disclose sensitive information. That said, the **Information Disclosure** in this scenario is not directly connected to the vulnerable app, but to the main star's poor privacy hygiene. Nevertheless, the app still functions as a tool that enables the **Information Disclosure**.

### What can go wrong?

Riotaro can bypass authorization controls by exploiting data flows between views, processes, and components to inject commands, manipulate data, or disclose sensitive information. He may deliver crafted deep links or intents from a malicious app or web page. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption.

Known threats include:

- **MAS-THREAT-0050:** Attackers can execute injection attacks against the app.
- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0059:** Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals).

This could be because:

- WebViews Allow Access to Local Resources with Untrusted Content: This weakness occurs when a WebView is configured to access local resources while also rendering untrusted content, allowing that content to reach files and data outside the web sandbox.
- Unsafe Handling of Untrusted Data: This weakness occurs when data originating outside the app's trust boundary reaches a sensitive sink without being validated, sanitized, or safely parsed.

### What are we going to do about it?

Treat every cross-component value as untrusted: use explicit, immutable intents and narrowly scoped IPC permissions, validate deep-link and WebView inputs against an allowlist, and test that crafted messages cannot invoke or disclose privileged data.

See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.
