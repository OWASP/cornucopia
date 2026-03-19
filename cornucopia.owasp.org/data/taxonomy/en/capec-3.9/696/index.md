# CAPEC™ 696: Load Value Injection

## Description

An adversary exploits a hardware design flaw in a CPU implementation of transient instruction execution in which a faulting or assisted load instruction transiently forwards adversary-controlled data from microarchitectural buffers. By inducing a page fault or microcode assist during victim execution, an adversary can force legitimate victim execution to operate on the adversary-controlled data which is stored in the microarchitectural buffers. The adversary can then use existing code gadgets and side channel analysis to discover victim secrets that have not yet been flushed from microarchitectural state or hijack the system control flow.

Source: [CAPEC™ 696](https://capec.mitre.org/data/definitions/696.html)

