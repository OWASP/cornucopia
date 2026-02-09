# CAPEC™ 323: TCP (ISN) Counter Rate Probe

## Description

This OS detection probe measures the average rate of initial sequence number increments during a period of time. Sequence numbers are incremented using a time-based algorithm and are susceptible to a timing analysis that can determine the number of increments per unit time. The result of this analysis is then compared against a database of operating systems and versions to determine likely operation system matches.

Source: [CAPEC™ 323](https://capec.mitre.org/data/definitions/323.html)

