## Technical Note: Martin can modify or expose sensitive data through unsafe reflection when reading data from public data storage (e.g. shared preferences) because the data is not validated before being read by the app

### Platform Guidance

**Android:** Never deserialize or reflect over attacker-controlled class names from shared preferences or external files; validate the schema first.

```kotlin
@Serializable data class Settings(val theme: String, val locale: String)
val settings = json.decodeFromString<Settings>(rawValue)
```

**iOS:** Use typed decoders and allowlists for externally sourced configuration instead of dynamic selector or class construction.

```swift
struct Settings: Decodable { let theme: String; let locale: String }
let settings = try JSONDecoder().decode(Settings.self, from: data)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0002
**New Tests:** MASTG-TEST-0231, MASTG-TEST-0298

### MASWE Weaknesses

- : unsafe reflection and validation gaps when reading public or mutable data stores.
