## Scenario: Jan's Crafty Payloads

Envision a situation where Jan, an astute intruder, manages to craft special payloads that circumvent input validation measures. He exploits several key weaknesses in the system:

1. **Unspecified/Unenforced Character Set:** The system fails to define or enforce a consistent character set for inputs.

2. **Multiple Encodings:** Data is encoded more than once, creating complexities that obscure malicious content.

3. **Inadequate Data Conversion (Canonicalization):** Data isn't fully converted into the format the application uses before being validated.

4. **Weak Typing of Variables:** Variables in the system are not strongly typed, allowing for type mismatches that can be exploited.

### Example

Jan targets the system by submitting a payload with characters that change meaning based on the character set. For instance, he uses a character set where certain symbols are interpreted differently, bypassing filters that would otherwise block malicious inputs. Due to the system not strictly enforcing a character set, or fully converting data into a consistent format, his payload is processed without proper validation, leading to potential security breaches.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE.
Crafting special/ambiguously encoded payloads to foil validation is an attack on the integrity of input data (i.e., tampering).
Jan is modifying the data semantics (by using alternate encodings, double-encoding, differing charset interpretations, etc.) so that filters/validators no longer recognize the malicious content.
STRIDE’s **Tampering** covers unauthorized modification or manipulation of data or how data is interpreted, which is exactly what character-set/canonicalization tricks do.

### What can go Wrong?

These vulnerabilities can result in severe security issues, such as injection attacks, data corruption, and unauthorized system access.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Prevent complications from multiple encodings by standardizing the encoding process.
2. Ensure complete data conversion into the application’s format (canonicalization) before validation.
3. Use strong typing for variables to prevent type-related security loopholes.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
