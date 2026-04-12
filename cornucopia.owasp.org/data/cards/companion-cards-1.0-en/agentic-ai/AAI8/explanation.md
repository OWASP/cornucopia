## Scenario: PreCursor's Unintended Code Execution via Weak Tool Input Validation

PreCursor can execute unintended code or system actions when tool input validation and sandboxing controls are weak. This occurs because:

1. **Insufficient input validation at the tool boundary:** Parameters passed from the agent to tools (code interpreters, shell commands, SQL engines) are not validated or sanitized before execution, allowing crafted inputs to break out of the intended command.

2. **Absent or permeable sandbox:** The execution environment for agent-invoked tools does not enforce strict isolation, so code that runs within a tool can access host resources, the file system, or the network beyond the intended scope.

3. **Overpermissioned execution context:** The process running the agent or its tools operates with more system privileges than necessary, amplifying the impact of any successful injection or escape.

### Example

PreCursor is an AI development assistant that can execute code snippets to help users debug programs. A malicious user submits a prompt asking the assistant to "run a quick test on this function" and includes code that opens a reverse shell to an external server. PreCursor passes the code to its execution tool without stripping dangerous system calls or confining execution to a restricted interpreter. The code runs successfully within the assistant's sandbox, which lacks network egress controls, and establishes an outbound connection to the attacker's infrastructure. The attacker now has interactive access to the environment where the AI assistant executes.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Elevation of Privilege**.

PreCursor's weak tool boundaries allow an attacker to escalate from a permitted AI interaction to arbitrary code execution on the underlying system. The attacker does not need to compromise authentication. They exploit the gap between what the tool is intended to execute and what it will actually execute when inputs are not constrained.

### What can go wrong?

Successful exploitation of weak sandboxing can give an attacker arbitrary code execution on the server or container running the agent. From there, lateral movement to other services, exfiltration of secrets and credentials, and persistent backdoor installation are all possible.

### What are we going to do about it?

Tool execution must be treated as the highest-risk action an agent can perform, with defense-in-depth applied at every layer of the execution stack.

1. Validate and allowlist tool input parameters before execution. Reject any input that does not conform to the expected type, length, and pattern.
2. Run tool execution in isolated containers or sandboxes with no access to the host file system, network (except explicitly allowed endpoints), or other processes.
3. Apply the principle of least privilege to the execution context. The process should run as a low-privilege user with no access to production credentials or sensitive environment variables.
4. Log all tool invocations with the exact parameters passed and the output returned, and alert on patterns consistent with escape attempts (e.g., network calls from a code execution context).
