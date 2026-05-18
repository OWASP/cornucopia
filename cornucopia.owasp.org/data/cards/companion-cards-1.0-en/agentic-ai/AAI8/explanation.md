## Scenario: PreCursor's Unintended Code Execution via Weak Tool Input Validation

PreCursor can execute unintended code or system actions when tool input validation and sandboxing controls are weak. This occurs because:

1. **Insufficient input validation at the tool boundary:** Parameters passed from the agent to tools (code interpreters, shell commands, SQL engines) are not validated or sanitized before execution, allowing crafted inputs to break out of the intended command.

2. **Absent or permeable sandbox:** The execution environment for agent-invoked tools does not enforce strict isolation, so code that runs within a tool can access host resources, the file system, or the network beyond the intended scope.

3. **Overpermissioned execution context:** The process running the agent or its tools operates with more system privileges than necessary, amplifying the impact of any successful injection or escape.

### Example

PreCursor is a Discord bot in a popular programming community that runs members' Python snippets so they can show off cool tricks and tiny bugs. A mischievous member submits "this totally cool one-liner I just want to test", a snippet that quietly opens a reverse shell to a laptop in their bedroom. PreCursor, with no input validation and a sandbox that has internet access, runs it without delay. Five minutes later, the member has interactive shell access to the bot's host server and is happily using it to mine cryptocurrency on the moderators' machine.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

PreCursor's weak tool boundaries allow an attacker to escalate from a permitted AI interaction to arbitrary code execution on the underlying system. The attacker does not need to compromise authentication. They exploit the gap between what the tool is intended to execute and what it will actually execute when inputs are not constrained.

### What can go wrong?

Successful exploitation of weak sandboxing can give an attacker arbitrary code execution on the server or container running the agent. From there, lateral movement to other services, exfiltration of secrets and credentials, and persistent backdoor installation are all possible.

For more things that can go wrong, see [OWASP Top 10 for LLM, Top 10 for Agentic Applications, and Mitre Atlas™](#mapping 'Companion edition requirement mapping [internal]') IDs in the mapping section below and correlate these with the IDs on the [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/), [OWASP Top 10 for Agentic Apps](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), and [Mitre Atlas™](https://atlas.mitre.org/techniques) websites.

### What are we going to do about it?

Tool execution must be treated as the highest-risk action an agent can perform, with defense-in-depth applied at every layer of the execution stack.

1. Validate and allowlist tool input parameters before execution. Reject any input that does not conform to the expected type, length, and pattern.
2. Run tool execution in isolated containers or sandboxes with no access to the host file system, network (except explicitly allowed endpoints), or other processes.
3. Apply the principle of least privilege to the execution context. The process should run as a low-privilege user with no access to production credentials or sensitive environment variables.
4. Log all tool invocations with the exact parameters passed and the output returned, and alert on patterns consistent with escape attempts (e.g., network calls from a code execution context).

For detailed advice on how to mitigate threats related to the card, see the [OWASP AISVS and OWASP AITG](#mapping 'OWASP AISVS and OWASP AITG tests requirements [internal]') IDs in the table below and correlate these with the IDs in the [OWASP AI Security Verification Standard](https://github.com/OWASP/AISVS/tree/main/1.0/en) and [OWASP AI Test Guide](https://github.com/OWASP/www-project-ai-testing-guide/tree/main/Document/content/tests) documentation.