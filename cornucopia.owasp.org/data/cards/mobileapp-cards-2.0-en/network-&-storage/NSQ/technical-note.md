## Technical Note: Ahmed can read and modify data in transit because the communication is transmitted over an unencrypted channel

### Platform Guidance

**Android:** Send sensitive traffic only over HTTPS or another authenticated encrypted channel; cleartext APIs are not “lightweight,” they are just loud.

```kotlin
val request = Request.Builder()
.url("https://api.example.com/profile")
.build()
```

**iOS:** Use `https://` endpoints everywhere, including image fetches, analytics, and sleepy legacy integrations.

```swift
let url = URL(string: "https://api.example.com/profile")!
let task = URLSession.shared.dataTask(with: url)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0019, MASTG-TEST-0065
**New Tests:** MASTG-TEST-0234, MASTG-TEST-0238, MASTG-TEST-0244, MASTG-TEST-0285, MASTG-TEST-0322, MASTG-TEST-0344, MASTG-TEST-0396

### MASWE Weaknesses

- MASWE-0050: unencrypted transport and exposure of data in transit.
