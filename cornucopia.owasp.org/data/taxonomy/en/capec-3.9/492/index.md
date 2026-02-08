# CAPEC™ 492: Regular Expression Exponential Blowup

## Description

An adversary may execute an attack on a program that uses a poor Regular Expression(Regex) implementation by choosing input that results in an extreme situation for the Regex. A typical extreme situation operates at exponential time compared to the input size. This is due to most implementations using a Nondeterministic Finite Automaton(NFA) state machine to be built by the Regex algorithm since NFA allows backtracking and thus more complex regular expressions.

Source: [CAPEC™ 492](https://capec.mitre.org/data/definitions/492.html)

