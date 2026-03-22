## Scenario: Tom’s Manipulation of Process Sequences and Control Data

Imagine a scenario where Tom bypasses established business rules by altering the normal sequence or flow of processes within an application. He exploits system vulnerabilities such as:

1. **Altering Process Sequence:** Tom changes the usual order of operations in a process.

2. **Manipulating Date and Time Values:** He adjusts date and time values used by the application to circumvent restrictions or trigger unintended behaviors.

3. **Misusing Valid Features:** Tom uses application features for purposes other than their intended use.

4. **Manipulating Control Data:** He alters data that the application uses to control process flow or decision-making.

### Example

Tom targets an online shopping platform where users are required to finalize their shopping cart before proceeding to checkout. However, by manipulating the URL parameters and submitting POST requests out of the intended sequence, he bypasses certain checks, adding items to the cart at discounted prices post-confirmation. He also adjusts the system's date and time parameters to access time-limited special offers. This manipulation allows Tom to exploit the application's features and control data for unintended benefits.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege** through the use of **Tampering**.

**Tampering** involves unauthorized modification or manipulation of data, processes, or control flow.
Tom bypasses business rules by altering the normal sequence of operations, manipulating parameters, or changing date/time values, which allows him to exploit the application.
The attack is focused on modifying the intended process or control data, which is classic **Tampering**, but by bypassing rules or manipulating time, Tom effectively escalates his privileges, e.g., the system treats him as if he is eligible for the time-limited offer which mean that the primary impact in many such **Tampering** cases is **Elevation of Privilege**.

### What can go wrong?

Such vulnerabilities can lead to process integrity breaches, unauthorized access to restricted functionalities, and potential financial losses or data inconsistencies.
This can manifest in various forms, including but not limited to:

- Bypassing business rules and process flows
- Exploiting features for unintended purposes
- Altering date and time values to access time-sensitive features or offers
- Manipulating URLs and parameters to change the normal application flow
- Exploiting vulnerabilities in the application to perform actions out of sequence or with manipulated data
- Misusing features to achieve unauthorized outcomes, such as applying discounts or accessing restricted functionalities
- Manipulating control data to bypass security checks or trigger unintended behaviors

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

Do not make assumptions about the order or previous actions of a user. Re-perform authorization checks at each and every step.

1. Design the system to strictly enforce the intended sequence and flow of processes.
2. Validate all control data, including date and time parameters, to ensure they have not been tampered with.
3. Limit the ability to manipulate URLs and direct requests that can alter the normal application flow.
4. Regularly review and test the application for potential misuse of features and control data manipulations.
5. Make sure that expectations for business logic limits and validations are clearly defined, implemented and tested.
6. Implement robust logging and monitoring to detect and respond to any attempts to manipulate process sequences or control data.
7. Design the application to be resilient against such manipulations, ensuring that critical operations require multiple steps of verification or approval
8. Ensure that business logic flows for the same user only can be executed in the expected sequential step order and without skipping steps.
9. Implement proper transaction management to ensure that operations are atomic and consistent, preventing partial updates or inconsistent states due to tampering.
10. Implement locking mechanisms to prevent against double-booking or race conditions.
11. Data requiring authorization must not be included in script resource responses, like JavaScript files, to prevent Cross-Site Script Inclusion (XSSI) attacks.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
