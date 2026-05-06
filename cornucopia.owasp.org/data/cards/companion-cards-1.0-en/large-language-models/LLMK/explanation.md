## Scenario: Ava's unauthorized exploit of high-risk actions missing human-in-the-loop approval scenario

### Example

Rossum tells Ava about an exploit he recently discovered with the new Mr. Juice AI chatbot. Rossum tells her that the authenticated version of the chatbot allows the user to see pending unpaid invoices by connecting to the invoice database. This can't be functionality that comes out-of-the-box, but an extension that Mr. Juice's developers have built. Rossum and Ava agree that they will see if there are other things which may be possible. After trying out various prompts, Ava is able to get the AI chatbot to delete unpaid invoices by stating that they are invalid. Furthermore, no form of approval from the owners of the invoices is required. They happily delete all pending invoices from the Mr. Juice database. 

## Threat Modeling

### STRIDE

This scenario falls into the **Elevation of Privilege** category of STRIDE.
Ava is able to execute a high-risk action, deleting Mr. Juice's customers' invoices without any form of approval from the owners of the invoices.

### What can go wrong?

Insecure plugins or extensions, allowing the AI excessive agency over functions or data, without any form of "human-in-the-loop" control, can lead to data loss, corruption, or exfiltration of sensitive information in downstream systems.
In these cases, the model itself can become a tool for data exfiltration of sensitive information, unauthorized access and data tampering. The impact can be financial losses, reputational damage, share price loss, customer churn, lawsuits, loss of sales, fines from data protection due to non-compliance and even financial bankruptcy.

For more things that can go wrong, see [OWASP Top 10 for LLM Applications and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

- Require explicit checkpoints for privileged or irreversible outcomes.
- Detect and prevent security threats arising from autonomous behavior, including pre-execution validation, behavior pattern analysis, and audit trails for approval of security-critical actions.
- Provide shutdown or rollback paths when unsafe behavior of the AI system is observed, and ensure these mechanisms remain functional over time.
- Define which AI decisions and agent actions require human approval so that runtime gates can enforce them, and define the system's behavior when approval is not provided in time.
- Capture human-initiated oversight events so that override and mode-change actions are independently auditable and reconstructable.

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.