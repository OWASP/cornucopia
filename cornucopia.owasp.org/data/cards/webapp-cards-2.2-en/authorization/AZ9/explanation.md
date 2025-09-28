## Scenario: Mike’s Misuse of Application Features

Envision a situation where Mike misuses an application by exploiting valid features in unintended ways. He leverages these features by:

1. **Excessive Speed or Frequency:** Using a feature too quickly or too frequently, beyond its normal operational capacity.

2. **Resource Consumption:** Utilizing features in a way that consumes excessive application resources.

3. **Inducing Race Conditions:** Performing actions in a manner that causes race conditions, where the application's behavior becomes unpredictable due to timing issues.

4. **Over-utilization of Features:** Exploiting a feature to an extent that it negatively impacts the application’s functionality or other users' experiences.

### Example

Mike discovers that an online booking system allows rapid repeated bookings and cancellations without any rate limits. He writes a script that continuously books and cancels appointments, exploiting the system’s lack of controls on the frequency of use. This not only consumes significant server resources, leading to performance degradation, but also creates race conditions that result in double bookings and data inconsistencies.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Denial of Service** (DoS).

**Denial of Service** occurs when an attacker causes a system to become unavailable, degrade performance, or otherwise disrupt normal operation.
Mike exploits a valid feature too quickly or too frequently, consuming server resources and creating race conditions, which affects availability and correctness.
The attack is focused on resource exhaustion and misuse of intended functionality, which aligns with the DoS category.

### What can go Wrong?

Such misuse can lead to system overloads, degraded performance, unintended application behaviors, and negative impacts on other users.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement rate limiting and usage throttling to prevent excessive use of features.
2. Design features with resource consumption and potential misuse in mind, ensuring they can handle unexpected or intensive usage without impacting overall system performance.
3. Regularly monitor application usage patterns to identify and address potential abuses or misuses of features.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
