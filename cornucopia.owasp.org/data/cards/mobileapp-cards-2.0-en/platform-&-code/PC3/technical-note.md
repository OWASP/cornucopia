## Technical Note: Harold can spy sensitive data being entered through the user interface because the data is excessive, not properly masked or cleaned up after use

### Platform Guidance

**Android:** Mask sensitive fields, disable autofill where appropriate, and clear one-time data from views after use so shoulder surfing and screen residue do not become a second feature.

```kotlin
passwordField.transformationMethod = PasswordTransformationMethod.getInstance()
passwordField.setAutofillHints(View.AUTOFILL_HINT_PASSWORD)
otpView.filters = arrayOf(InputFilter.LengthFilter(6))
otpView.doAfterTextChanged { value ->
if (value?.length == 6) otpView.text?.clear()
}
```

**iOS:** Prefer `SecureField` / `isSecureTextEntry`, keep sensitive values out of reusable view models, and clear temporary UI state when the task ends.

```swift
let passwordField = UITextField()
passwordField.isSecureTextEntry = true
passwordField.textContentType = .password

func clearOneTimeCode() {
otpTextField.text = nil
view.endEditing(true)
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0008, MASTG-TEST-0037, MASTG-TEST-0057
**New Tests:** MASTG-TEST-0251, MASTG-TEST-0294, MASTG-TEST-0357, MASTG-TEST-0277, MASTG-TEST-0335, MASTG-TEST-0378

### MASWE Weaknesses

- MASWE-0054, MASWE-0062, MASWE-0071: sensitive user-interface handling, masking, and cleanup of secrets that linger in presentation layers.
