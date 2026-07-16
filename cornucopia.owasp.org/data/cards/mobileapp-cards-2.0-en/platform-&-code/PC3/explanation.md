## Scenario: Harold can spy on sensitive data being entered through the user interface because the data is excessive, not properly masked, or not cleaned up after use

Consider a scenario where Harold borrows a colleague's phone for a moment. The healthcare app on the device has a search field that autocompletes medication names, because the developer thoughtfully wanted to help users who can't spell "cephalexin." Harold types a single letter and the keyboard's suggestion bar offers a list of medical terms previously entered by the device's owner. He did not hack anything. The app handed him a summary of someone's prescription history through the autocomplete cache.

1. Keyboard caches typed text and surfaces it as suggestions in other apps.
2. Sensitive fields not marked as password-type allow third-party keyboards to record and transmit input.
3. Values displayed in cleartext without masking are visible to shoulder-surfers or screen recordings.
4. Data left on the clipboard remains readable by any app or the next person to use the device.

### Example

Nizhoni uses a healthcare app to record her prescriptions. The app's medication-name field does not disable autocomplete. The next time she opens a browser on the same device, the keyboard suggests her medication names when she types the first few letters. Her roommate borrows the phone, types something innocuous, and is presented with a helpful list of Nizhoni's medications as suggestions. Nizhoni's medical privacy has been effectively crowd-sourced to whoever touches the keyboard next.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Sensitive data is passively surfaced to unintended parties through platform UI features — autocomplete, keyboard cache, clipboard — that the app failed to suppress. No network traffic or active exploitation is required.

### What can go wrong?

- Keyboard caches store typed text and expose it through autocomplete across all apps.
- Third-party keyboards with network access can exfiltrate keystrokes to remote servers.
- Unmasked sensitive fields are captured by shoulder-surfing, screen recordings, and accessibility services.
- Clipboard content persists after the user leaves the app and is readable by any app or subsequent user.

### What are we going to do about it?

- Mark all sensitive input fields (passwords, PINs, OTPs, card numbers) with the platform's secure-text flag to disable keyboard caching and autocomplete.
- Mask displayed values by default; provide a "show" toggle only on explicit user request, and re-mask after a short timeout.
- Clear clipboard content after a brief interval (30 seconds is a common baseline) when the app copies sensitive data.
- Restrict third-party keyboard usage for the most sensitive screens where the platform allows it.
- Clear sensitive text from memory as soon as it is no longer needed.
