## Scenario: Martin can modify or expose sensitive data through unsafe reflection when reading data from public data storage because the data is not validated before being read by the app

Consider a scenario where Martin discovers the app reads a configuration class name from a `SharedPreferences` entry and instantiates it using Java reflection: `Class.forName(className).newInstance()`. Martin modifies `SharedPreferences` on a rooted device to substitute a class name of his choosing. The app instantiates Martin's class, which executes arbitrary code in the app's process context.

1. Reflection with class names from untrusted sources allows an attacker to instantiate arbitrary classes.
2. Untrusted data read from public storage and used to control application behaviour (e.g., feature flags, config values) is a manipulation surface.

### Example

Martin modifies the app's `SharedPreferences` XML on a rooted device to change `config_class=com.target.app.DefaultConfig` to `config_class=com.target.app.debug.AdminConfig`. The `AdminConfig` class is present in the APK (it was never removed from the release build) and has a static initializer that grants admin privileges. The app reads the value from storage and instantiates the class via reflection. Martin now has admin access. The developer left debug code in the release build and trusted local storage as a configuration source without validation.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

Martin manipulates data in public or device-accessible storage that the app trusts without validation, causing the app to execute unintended code or apply incorrect configuration — effectively allowing him to alter the app's behaviour to his advantage.

### What can go wrong?

- Reflection on attacker-controlled class names allows arbitrary code execution.
- Configuration data from accessible storage can be modified to change app behaviour, disable security controls, or activate hidden features.
- Object deserialization gadget chains can be triggered by substituting class names or serialized object values.

### What are we going to do about it?

- Never use data from untrusted or publicly accessible storage to control reflection, class loading, or deserialization.
- Validate all data read from `SharedPreferences`, external storage, or other accessible locations before use; apply strict allowlists.
- Remove debug and development classes from release builds so that they cannot be instantiated even if an attacker controls the class name.
- If configuration must be loaded from a file, sign the configuration and verify the signature before applying it.
