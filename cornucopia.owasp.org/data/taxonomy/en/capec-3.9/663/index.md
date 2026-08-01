# CAPEC™ 663: Exploitation of Transient Instruction Execution

## Description

An adversary exploits a hardware design flaw in a CPU implementation of transient instruction execution to expose sensitive data and bypass/subvert access control over restricted resources. Typically, the adversary conducts a covert channel attack to target non-discarded microarchitectural changes caused by transient executions such as speculative execution, branch prediction, instruction pipelining, and/or out-of-order execution. The transient execution results in a series of instructions (gadgets) which construct covert channel and access/transfer the secret data.

Source: [CAPEC™ 663](https://capec.mitre.org/data/definitions/663.html)

