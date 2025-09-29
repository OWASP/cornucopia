## Scenario: Lee's Bypassing of Application Controls

Imagine a scenario where Lee bypasses application controls due to various coding and implementation vulnerabilities. This situation arises from:

1. **Use of Risky Programming Functions:** The application utilizes dangerous functions in its code instead of safer alternatives.
2. **Type Conversion Errors:** Inaccurate or improper type conversions lead to vulnerabilities.
3. **Dependency on External Resources:** The application’s reliability is compromised when external resources are unavailable.
4. **Race Conditions:** Concurrent processes lead to conditions where the application’s behavior is unpredictable.
5. **Resource Initialization or Allocation Issues:** Problems in initializing or allocating resources create vulnerabilities.
6. **Potential for Overflows:** The application is susceptible to overflows, such as buffer overflows, due to inadequate handling.

### Example

Lee discovers that a web application uses risky functions that are known to be vulnerable to injection attacks. He exploits these functions to manipulate the application’s behavior. Additionally, Lee takes advantage of type conversion errors to cause unexpected behaviors in the application. He also notices that the application fails to handle scenarios where an external API is down, using this to trigger a denial of service. Furthermore, Lee exploits a race condition by initiating simultaneous processes that alter the application’s intended flow, and he triggers a buffer overflow to execute arbitrary code.

## Threat Modeling

### STRIDE

The applicable STRIDE category here is primarily **Tampering**, with potential secondary impacts depending on the specific exploitation.

Lee is altering or influencing the application’s behavior through exploitation of unsafe code patterns, type conversion errors, race conditions, and overflows.
**Tampering** in STRIDE covers unauthorized modification of data or code or causing the application to behave differently than intended, which is what occurs here.
Exploiting buffer overflows or unsafe functions to inject malicious code directly falls under **Tampering**.

### What can go wrong?

Such vulnerabilities can lead to a range of issues, from unauthorized access and data breaches to complete system compromise.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Replace risky functions with safer alternatives and follow secure coding practices.
2. Implement thorough error handling and validation for type conversions.
3. Design the application to handle unavailability or failures of external resources gracefully.
4. Address potential race conditions through proper synchronization and concurrency controls.
5. Ensure robust initialization and allocation of resources, and rigorously check for potential overflows.
6. Regularly audit and test the application for these vulnerabilities, and update practices as needed.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
