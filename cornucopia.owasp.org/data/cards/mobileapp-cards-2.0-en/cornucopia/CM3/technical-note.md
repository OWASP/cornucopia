## Technical Note: Elsa can reduce app users' privacy because the app does not allow for the user to easily manage, delete and modify their data, change privacy settings and re-prompt for consent when more data is required

### Platform Guidance

**Android:** Provide user-facing controls to export, correct, and delete stored data, and make the backend actually perform the same action instead of sending polite vibes.

```kotlin
lifecycleScope.launch {
api.deleteAccountData()
localStore.purgeUserData()
}
```

**iOS:** Include privacy settings, deletion workflows, and consent refresh paths that are as easy to find as the feature that collected the data.

```swift
func deleteMyData() async throws {
try await api.deleteProfile()
try secureStore.wipe()
}
```

### Relevant Tests

**Legacy Tests:** -
**New Tests:** MASTG-TEST-0254, MASTG-TEST-0319, MASTG-TEST-0363

### MASWE Weaknesses

- MASWE-0109, MASWE-0114: weak privacy controls for data management, deletion, and user agency.
